/*************************************************
*	FUNCTION NAME : SerialIo.nc
*	FUNCTION DESCRIPTION : 串口输入输出示例程序，可从串口接收和显示数据
*	FUCNTION DATE :2010/10/15
*	FUNCTION AUTHOR: EMDOOR
**/

configuration SerialIo
{
}
implementation
{
	components SerialIoM;  /* SerialIo模块程序，用于实现具体代码 */
	components MainC;  	   /* TinyOS主模块，这里用于关联系统启动 */
	components LedsC;	   /* Led模块程序，提供对LED的控制*/

	/** SerialIo模块程序的Boot接口与系统Boot接口关联
	    这样系统启动时会调用SerialIoM的Boot接口
	*/
	SerialIoM.Boot -> MainC.Boot;
	
	/**串口模块程序与Led模块关联
	*
	*/
	
	SerialIoM.Leds -> LedsC;
	
	/** PlatformSerialC
	*/
	components PlatformSerialC;
	SerialIoM.CC2430UartControl -> PlatformSerialC.CC2430UartControl;
	SerialIoM.UartStdControl -> PlatformSerialC.UartStdControl;
	SerialIoM.UartStream -> PlatformSerialC.UartStream;
}
