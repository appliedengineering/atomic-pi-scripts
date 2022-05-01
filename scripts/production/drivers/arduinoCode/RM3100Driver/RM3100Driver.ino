// RM3100 SPI Communication For Arduino
// Applied Engineering 2022

/*
 * This code represents a serial driver for the RM3100 and ADXL343 modules
 *
 * Protocol
 *
 * In order to retrieve compass reading, send the bytes of a *capital* M
 * device will respond with the compass reading as a float
 *
 * If USE_SERVO is set to true, the following apply
 * to turn servo right, send the bytes of a capital R
 * to turn servo left, send the bytes of a capital L
 */

#include <SPI.h>
#include <Servo.h>
#include <Adafruit_ADXL343.h>

Adafruit_ADXL343 accel = Adafruit_ADXL343(12345);

#define USE_SERVO true

#ifdef USE_SERVO
Servo servo;
#endif

// slave select pin
#define SS_PIN 10
// MOSI (send data from master to slave)
#define MOSI_PIN 11
// MISO (send data from the slave to master)
#define MISO_PIN 12
// SCK (the clock)
#define SCK_PIN 13
// DRDY (data ready pin)
#define DRDY_PIN 6

// CALIBRATION VALUES
int X_MID = 1871 + -2350; // (MAX + MIN)
int Y_MID = 1612 + -2674;
int Z_MID = 1672 + -1274;

// READ COMMAND
const byte READ = 0b10000000;
const byte WRITE = 0b00000000;

const int BYTES_TO_READ = 9;

// data buffer
byte bufferData[BYTES_TO_READ];

int maxData[3] = {0, 0, 0};
int minData[3] = {0, 0, 0};

// REGISTER ADDRS
#define POLL_REG 0x00
#define CCM_REG 0x01
#define READ_REG 0x24

#ifdef USE_SERVO
int servoRotation = 0; // -1 = left, 0 = none, 1 = right
#endif

int targetAngle = 30;
int allowance = 20;

void setup()
{
    // put your setup code here, to run once:
    Serial.begin(9600);
    SPI.begin();
    pinMode(DRDY_PIN, INPUT);
    pinMode(SS_PIN, OUTPUT);

#ifdef USE_SERVO
    servo.attach(5);
#endif

    accel.begin();
    accel.setRange(ADXL343_RANGE_16_G);

    // disable the slave
    digitalWrite(SS_PIN, HIGH);

    delay(500); // bc the drdy pin is broken
}

void loop()
{

    if (Serial.available() > 0)
    {
        // read the incoming byte
        delay(10);
        int readTargetAngle = Serial.parseFloat();
        // throw away extra bytes
        Serial.read();
        Serial.read();

        Serial.print("Target Angle: ");
        Serial.println(readTargetAngle);
        targetAngle = readTargetAngle;
    }

    float readAngle = takeAverageMeasurement();
    Serial.println(readAngle);

    float headingDelta = readAngle - targetAngle;

    if (abs(headingDelta) > 180)
    {
        if (headingDelta < 0)
        {
            headingDelta += 360;
        }
        else
        {
            headingDelta -= 360;
        }
    }

    if (abs(headingDelta) < allowance)
    {
        servoRotation = 0;
        Serial.println("M");
    }
    else if (headingDelta < 0)
    {
        servoRotation = -1;
        Serial.println("L");
    }
    else
    {
        servoRotation = 1;
        Serial.println("R");
    }
    delay(0);
#ifdef USE_SERVO
    handleServo();
#endif
}
#ifdef USE_SERVO
void handleServo()
{
    if (servoRotation == 0)
    {
    }
    else if (servoRotation == -1)
    {
        servo.write(66);
    }
    else if (servoRotation == 1)
    {
        servo.write(121);
    }
}
#endif
float takeAverageMeasurement()
{
    // take 5 measurements and average them
    float average = 0;
    int samples = 5;

    for (int i = 0; i < samples; i++)
    {
        average += takeCompassMeasurement();
    }
    average /= (float)samples;
    return average;
}

int takeCompassMeasurement()
{
    // initiate continous measurement mode
    writeRegister(POLL_REG, 0x70);

    // blocking loop to wait for data
    while (digitalRead(MISO_PIN) != LOW)
        ;
    delay(10);
    // data is ready
    readRegister(READ_REG, BYTES_TO_READ); // 3 bytes for each axis

    int intData[3];

    // the chip outputs data in 24 bit resolution!!!
    // 3 bytes per int
    for (int i = 0; i < BYTES_TO_READ / 3; i++)
    {
        byte axisComponent[3];
        for (int byteNum = 0; byteNum < 3; byteNum++)
        {
            axisComponent[byteNum] = bufferData[3 * i + byteNum];
        }

        // process axis component
        // MSB
        unsigned int num = 0;

        // perform bit shifts
        unsigned int byte1 = axisComponent[0] << (8 * 2);
        unsigned int byte2 = axisComponent[1] << (8 * 1);
        unsigned int byte3 = axisComponent[2];

        num = byte1 + byte2 + byte3;
        // convert to signed
        int signedInt = num;
        intData[i] = num;

        maxData[i] = max(intData[i], maxData[i]);
        minData[i] = min(intData[i], minData[i]);
    }

    // Serial.println(intData[0]);
    // Serial.println(intData[1]);

    float calibratedY = intData[1] - (maxData[1] + minData[1]) / 2.0;
    float calibratedX = intData[0] - (maxData[0] + minData[0]) / 2.0;
    float calibratedZ = intData[2] - (maxData[2] + minData[2]) / 2.0;

    // TILT COMPENSATION
    sensors_event_t event;
    accel.getEvent(&event);

    float y_accel, x_accel, z_accel;

    x_accel = event.acceleration.x;
    y_accel = event.acceleration.y;
    z_accel = event.acceleration.z;

    // Serial.print(x_accel);Serial.print("  ");
    // Serial.print(y_accel);Serial.print("  ");
    // Serial.println(z_accel);

    float roll = atan2(y_accel, z_accel);
    float pitch = atan2((-x_accel), sqrt(y_accel * y_accel + z_accel * z_accel));
    float compensatedX = calibratedX * cos(pitch) + calibratedZ * sin(pitch);
    float compensatedY = calibratedX * sin(roll) * sin(pitch) + calibratedY * cos(roll) - calibratedZ * sin(roll) * cos(pitch);

    // Serial.print("Angle:");

    float angle = atan2(-compensatedY, compensatedX) / PI * 180;
    // float angle2 = atan2(-calibratedY, calibratedX)/PI*180;
    // Serial.println(((int)angle2 + 180)%360);
    return ((int)angle + 180) % 360;
}

void readRegister(byte thisRegister, int bytesToRead)
{
    digitalWrite(SS_PIN, LOW);

    // Serial.print(thisRegister, BIN);

    // RM3100 expects the register address in the lower 7 bits

    // of the byte and a 1 in the first bit

    // so add 0x80 to the register byte

    thisRegister += 0x80;

    SPI.transfer(thisRegister); // init the register for read

    for (int i = 0; i < bytesToRead; i++)
    {
        bufferData[i] = SPI.transfer(0x00);
    }

    digitalWrite(SS_PIN, HIGH);
}

void writeRegister(byte thisRegister, byte thisValue)
{

    // RM3100 expects the register address in the lower 7 bits

    // of the byte. So shift the bits right by 1 bit

    thisRegister = thisRegister << 1;

    // now combine the register address and the command into one byte:
    // note the pipe operator
    byte dataToSend = WRITE | thisRegister;

    // take the chip select low to select the device:

    digitalWrite(SS_PIN, LOW);

    SPI.transfer(dataToSend); // Send register location

    SPI.transfer(thisValue); // Send value to record into register

    // take the chip select high to de-select:

    digitalWrite(SS_PIN, HIGH);
}
