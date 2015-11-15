/* University of Brasília - Campus Gama
 * Integration Project II - 2º/2015
 *
 * This script is used to control the duty cycle of a PWM using an ADC.
 * Input: analog signal (potentiometer) in P1.5
 * Output: PWM signal in P1.6 (green LED on LaunchPad)
 */

// Headings
#include <msp430.h>

// Definitions
#define RLED BIT0
#define GLED BIT6
#define BTN BIT3
#define RXPIN BIT1
#define TXPIN BIT2
#define AD_IN (BIT5)
#define AD_CH INCH_5

// Global variables
int samples[2];

// Prototypes
void ad_config();
void uart_config();
void port1_config();
void send_data();

// Main
int main() {
	WDTCTL = WDTPW + WDTHOLD; // Stop WDT
	BCSCTL1 = CALBC1_1MHZ; // Set DCO
	DCOCTL = CALDCO_1MHZ;

	ad_config();
	uart_config();
	port1_config();

	while(1) {
		// Set block start address
		ADC10SA = (int)&samples[0];
		// Start conversion
		ADC10CTL0 |= ADC10SC + ENC;
		_BIS_SR(LPM0_bits+GIE);
		send_data();
	}

	return 0;
}

// ADC10 interruption controller
void ADCInt(void) __attribute__((interrupt(ADC10_VECTOR)));
void ADCInt(void) {
	ADC10CTL0 &= ~(ADC10SC+ENC);
	LPM0_EXIT;
}

// Send ADC values via UART
void send_data() {
	volatile unsigned char x = 0xFF & (samples[0] >> 2);
	P1OUT ^= GLED + RLED;
	if(x < 127) {
		while (!(IFG2 & UCA0TXIFG));
		UCA0TXBUF = x | 0x01;
		while (!(IFG2 & UCA0TXIFG));
		UCA0TXBUF = x & 0xFE;
	}
}

// Initialize ADC10
void ad_config() {
	// Turn off ADC10 for setting it up
	ADC10CTL0 &= ~ENC;
	//          Vcc/GND  s&h=16clks   I.E.      ADC ON    Automatically enable next conversion
	ADC10CTL0 = SREF_0 + ADC10SHT_2 + ADC10IE + ADC10ON + MSC;
	//          INCH     /1           SMCLK         repeat-seq-of-conversion
	ADC10CTL1 = AD_CH +  ADC10DIV_0 + ADC10SSEL_3 + CONSEQ_3;
	// Two conversions
	ADC10DTC1 = 8;
	// Set analog inputs
	ADC10AE0 |= AD_IN;
	// Turn on ADC10
	ADC10CTL0 |= ENC;
}

// Initialize UART
void uart_config() {
	// LSB first - 8-bit data - no parity - 1 stop bit - UART - Async
	UCA0CTL0 = 0;
	// SMCLK
	UCA0CTL1 = UCSSEL_2;
	// baud rate 9600
	UCA0BR0 = 6;
	UCA0BR1 = 0;
	// ?
	UCA0MCTL = UCBRF_8 + UCOS16;
}

// Initialize Port1
void port1_config() {
	// Initial setup
	P1DIR = RLED + GLED;
    P1SEL = RXPIN + TXPIN + RLED;
	P1SEL2 = RXPIN + TXPIN;
	P1OUT = GLED;
}
