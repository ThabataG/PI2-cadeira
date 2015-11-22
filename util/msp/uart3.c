#include <msp430.h>  
#include <stdint.h>

int main()  
{  
    WDTCTL = WDTPW + WDTHOLD;     
    BCSCTL1 = CALBC1_1MHZ;  
    DCOCTL = CALDCO_1MHZ;  
    
    UCA0CTL0 = 0;
	UCA0CTL1 = UCSSEL_2; // SMCLK
	UCA0BR0 = 6; // 1MHz 9600 //0x08 1MHz 115200
	UCA0BR1 = 0; // 1MHz 115200
	UCA0MCTL = UCBRF_8 + UCOS16;

    P1SEL2 = P1SEL = BIT1 | BIT2;
	P1IE = P1IES = P1OUT = P1REN = BIT3;
	P1IFG &= ~BIT3;      
   
    P1DIR |= BIT0 | BIT6;  
    P1OUT = BIT0;
  
    __bis_SR_register(GIE);  
    while(1);
  
    return 0;  
}

void Port1Int(void) __attribute__((interrupt(PORT1_VECTOR)));  
void Port1Int(void)  
{
	/*const char string[] = {"Hello World\r\n"};
	int i;
	for(i=0;i<13;i++) {
		while (!(IFG2 & UCA0TXIFG));	// USCI_A0 TX buffer ready?
		UCA0TXBUF = string[i]; // TX next character 
	}*/
 
 	while (!(IFG2 & UCA0TXIFG));
	UCA0TXBUF = 'a';
	while (!(IFG2 & UCA0TXIFG));
	UCA0TXBUF = '\n';
 
 	P1OUT ^= BIT0 + BIT6;
	P1IFG &= ~BIT3;	
}

