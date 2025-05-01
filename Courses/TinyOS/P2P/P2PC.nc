/*************************************************
*	FUNCTION NAME : P2PC.nc
*	FUNCTION DESCRIPTION : 点对点射频通信
*	FUCNTION DATE :2010/10/18
*	FUNCTION AUTHOR: EMDOOR
**/

configuration P2PC
{
}
implementation
{
	components P2PM;
	components MainC;
	P2PM.Boot -> MainC.Boot;
	
	components LedsC;
	P2PM.Leds -> LedsC;

	/* 串口收发组件*/
	components PlatformSerialC;
	P2PM.UartStdControl -> PlatformSerialC;
	P2PM.UartStream -> PlatformSerialC;

	/*活动消息组件*/
	components ActiveMessageC;
	P2PM.RFControl -> ActiveMessageC;
	P2PM.AMPacket -> ActiveMessageC;
	P2PM.Packet -> ActiveMessageC;

	#define AM_DATA_TYPE 220

	P2PM.AMSend -> ActiveMessageC.AMSend[AM_DATA_TYPE];
	P2PM.Receive -> ActiveMessageC.Receive[AM_DATA_TYPE];
}
