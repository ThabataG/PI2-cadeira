#include <msp430.h>

#define LED1 BIT0
#define LED2 BIT6

// GLOBAL VARIABLES
volatile unsigned int latest_adc_result;

// FUNCTION PROTOTYPES
void init_led();
void init_uart();
void init_adc();
void start_conversion();

// MAIN FUNCTION
void main(void) {
	// clock initializers
	WDTCTL 	 = WDTPW + WDTHOLD;	// stop the WDT
	BCSCTL1  = CALBC1_16MHZ;	 	// calibration for basic clock system
	DCOCTL 	 = CALDCO_16MHZ;	 	// calibration for digitally controlled oscillator

	// initiate peripherals
	//init_led();
	init_uart();
	//init_adc();

	// enable interrupts and put the CPU to sleep
	IE2 |= UCA0TXIE;
	__bis_SR_register(GIE); // Enter LPM0 w/ int until Byte RXed
  while (1);
}

// HELPER FUNCTIONS
void init_led() {
	P1DIR = LED1 + LED2;
	P1OUT = 0;
}

void init_uart() {
	P1SEL  = BIT1 + BIT2;	// P1.1 = RXD, P1.2 = TXD
	P1SEL2 = BIT1 + BIT2;	// P1.1 = RXD, P1.2 = TXD
	UCA0CTL1 |= UCSSEL_2;	// SMCLK
	UCA0BR0 = 130;//26;//104;					// see baud rate divider above
	UCA0BR1 = 6;//0;
	UCA0MCTL = UCBRS2+UCBRS1;//UCBRS0;			// modulation UCBRSx = 1
	UCA0CTL1 &= ~UCSWRST;	// ** initialize USCI state machine **
	IE2 |= UCA0TXIE;		// Enable USCI_A0 TX interrupt
}

void init_adc() {
	ADC10CTL1 = INCH_3		// pin 1.3 input to ADC
			+ SHS_0			// use ADC10SC bit to trigger sampling
			+ ADC10DIV_0	// clock divider = 1
			+ ADC10SSEL_3	// clock source = SMCLK
			+ CONSEQ_0;		// single channel, single conversion
	ADC10DTC1 = 1;			// one block per transfer

	ADC10CTL0 = SREF_0		// reference voltages are Vss and Vcc
			+ ADC10SHT_0	// 64 ADC10 clocks for sample and hold time (slowest)
			+ ADC10ON		// turn on ADC10
			+ ENC;			// enable (but not yet start) conversions
}

void start_conversion() {
	if ((ADC10CTL1 & ADC10BUSY) == 0) {	// if not already converting
		P1OUT ^= LED2;
		ADC10CTL0 |= ADC10SC;
		ADC10SA = (unsigned) &latest_adc_result;
	}
}

// INTERRUPT HANDLERS
#pragma vector=USCIAB0TX_VECTOR
__interrupt void USCI0TX_ISR(void) {
	//start_conversion();

	while (!(IFG2 & UCA0TXIFG));	// USCI_A0 TX buffer ready?
	UCA0TXBUF = 'a';

	IE2 &= ~UCA0TXIFG;
	IE2 |= UCA0TXIE;
}

