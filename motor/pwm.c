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
#define CYCLE 0xF	// PWM frequency = SMCLK / CYCLE
#define AD_IN BIT5
#define AD_CH INCH_5
#define ADC_MAX 0x4FF

// Prototypes
void ad_config();
void timerA_config();
void port1_config();

// Main
int main() {
	WDTCTL = WDTPW + WDTHOLD; // Stop WDT
	BCSCTL1 = CALBC1_1MHZ; // Set DCO
	DCOCTL = CALDCO_1MHZ;

	ad_config();
	timerA_config();
	port1_config();
	
	while(1) {
		ADC10CTL0 |= ADC10SC;
		_BIS_SR(LPM0_bits+GIE);
	}
	
	return 0;
}

// ADC10 interruption controller
void ADCInt(void) __attribute__((interrupt(ADC10_VECTOR)));
void ADCInt(void) {
	ADC10CTL0 &= ~ADC10SC;
	TACCR1 = CYCLE * ADC10MEM / ADC_MAX;
	LPM0_EXIT;
}

// Initialize ADC10
void ad_config() {
	// Set analog input
	ADC10AE0 = AD_IN;
	//          BIT5	   /1           SMCLK         single-ch-repeat-conversion
	ADC10CTL1 = AD_CH +  ADC10DIV_0 + ADC10SSEL_3 + CONSEQ_2;
	//          Vcc/GND  s&h=4clks    I.E.      ADC ON    Enable Conversion
	ADC10CTL0 = SREF_0 + ADC10SHT_0 + ADC10IE + ADC10ON + ENC;
}

// Initialize TimerA
void timerA_config() {
	// It's a good practice to stop timer before changing its configuration
	TACTL = MC_0;
	// Period
	TACCR0 = CYCLE-1;
	// Duty cycle
	TACCR1 = CYCLE/4;
	// Output mode 7: reset/set
	TACCTL1 = OUTMOD_7;
	//      SMCLK      /1     upmode
	TACTL = TASSEL_2 + ID_0 + MC_1;
}

// Initialize Port1
void port1_config() {
	// Initial setup
	P1DIR = RLED + GLED;
	P1SEL |= GLED;
	// Initial state of leds
	P1OUT |= RLED;
}

