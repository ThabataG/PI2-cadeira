#include <msp430.h>

#define TXLED BIT0
#define RXLED BIT6
#define BTN BIT3
#define TX BIT2
#define RX BIT1

const char string[] = { "Hello World\r\n" };

int main(void)
{
  WDTCTL = WDTPW + WDTHOLD; // Stop WDT
  DCOCTL = 0; // Select lowest DCOx and MODx settings
  BCSCTL1 = CALBC1_1MHZ; // Set DCO
  DCOCTL = CALDCO_1MHZ;

  P2DIR |= 0xFF; // All P2.x outputs
  P2OUT &= 0x00; // All P2.x reset
  P1SEL2 = P1SEL = RX+TX;
  P1DIR = RXLED + TXLED;
  P1IE = P1IES = P1OUT = P1REN = BTN;
  P1IFG &= ~BTN;

  UCA0CTL0 = 0;
  UCA0CTL1 = UCSSEL_2; // SMCLK
  UCA0BR0 = 6; // 1MHz 9600 //0x08 1MHz 115200
  UCA0BR1 = 0; // 1MHz 115200
  UCA0MCTL = UCBRF_8 + UCOS16;
	//IE2 |= UCA0RXIE; // Enable USCI_A0 RX interrupt

  //   __bis_SR_register(GIE); // Enter LPM0 w/ int until Byte RXed

  P1OUT = TXLED;
  _BIS_SR(LPM0_bits+GIE);
  while(1);

  return 0;
}

void Port1Int(void) __attribute__((interrupt(PORT1_VECTOR)));
void Port1Int(void)
{
	int i=0;
	P1OUT ^= TXLED+RXLED;
//	while (1) {
        while (!(IFG2 & UCA0TXIFG));	// USCI_A0 TX buffer ready?
        UCA0TXBUF = 'a'; // TX next character

        while (!(IFG2 & UCA0TXIFG));	// USCI_A0 TX buffer ready?
        UCA0TXBUF = '\n'; // TX next character

        for(i =0; i< 10000; i++);
//        if(i == 13) break;
//    }
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
