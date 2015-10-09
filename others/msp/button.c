#include <msp430.h>
 
#define RLED BIT0
#define GLED BIT6
#define BTN BIT3
#define DLY 10000

// Prototypes
void port1_config();
void delay(volatile unsigned int t);

int main(void)
{
	WDTCTL = WDTPW + WDTHOLD; // Stop WDT
	BCSCTL1 = CALBC1_1MHZ; // Set DCO
	DCOCTL = CALDCO_1MHZ;

	port1_config();

	while(1) _BIS_SR(LPM0_bits+GIE);
	
	return 0;
}

void Port1Int(void) __attribute__((interrupt(PORT1_VECTOR)));  
void Port1Int(void)  
{
	P1OUT ^= RLED + GLED;
	delay(DLY);
	P1IFG = 0;
}

/*
#pragma vector=USCIAB0TX_VECTOR
__interrupt void USCI0TX_ISR(void)
{
	//P1OUT |= TXLED;
	while (!(IFG2 & UCA0TXIFG));	// USCI_A0 TX buffer ready?
	
	UCA0TXBUF = 'a';//string[i++]; // TX next character 
	//if (i == sizeof string - 1) // TX over? 
		UC0IE &= ~UCA0TXIE; // Disable USCI_A0 TX interrupt 
	P1OUT &= ~TXLED;
}

#pragma vector=USCIAB0RX_VECTOR
__interrupt void USCI0RX_ISR(void) 
{ 
   P1OUT |= RXLED; 
    if (UCA0RXBUF == 'a') // 'a' received?
    { 
       	i = 0; 
       	UC0IE |= UCA0TXIE; // Enable USCI_A0 TX interrupt 
		UCA0TXBUF = 'a';//string[i++]; 
    } 
    P1OUT &= ~RXLED;
}
*/

void port1_config() {
	// Initial setup
	P1SEL2 = P1SEL = 0;
	P1OUT = P1REN = BTN;
	P1DIR = RLED + GLED;
	
	// Interruption setup
	P1IE = P1IES = BTN;
	
	// Initial state of leds
	P1OUT |= RLED;
}

void delay(volatile unsigned int t) {
	volatile unsigned int i;
	for(i=0; i<t; i++);
}








