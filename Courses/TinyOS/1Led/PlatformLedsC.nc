configuration PlatformLedsC
{
  provides interface GeneralIO as RedLed;
  provides interface GeneralIO as BlueLed;
  provides interface GeneralIO as YellowLed;
#ifdef USE_BOARD_LED
  provides interface GeneralIO as BoardRedLed;
  provides interface GeneralIO as BoardBlueLed;
  provides interface GeneralIO as BoardGreenLed;
  provides interface GeneralIO as BoardYellowLed;
#endif

  uses interface Init;
}
implementation
{
  components HplCC2430GeneralIOC as CC2430IO;
  components PlatformP;

  // Let LedsP (from system) handle the Led init...
  Init = PlatformP.LedsInit;

  /* 
   * The bizare Led interface assumes that the led pins are active
   * high...
   */

	BlueLed		= CC2430IO.P12;
	RedLed		= CC2430IO.P13;
	YellowLed	= CC2430IO.P20;	

#ifdef USE_BOARD_LED	
	BoardGreenLed	= CC2430IO.P11;  
	BoardBlueLed	= CC2430IO.P10;
	BoardRedLed	= CC2430IO.P01;
	BoardYellowLed	= CC2430IO.P14;
#endif
}

