/*************************************************
*	FUNCTION NAME : SerialIoM.nc
*	FUNCTION DESCRIPTION :
*	FUCNTION DATE :2010/10/15
*	FUNCTION AUTHOR: EMDOOR
**/

#include <strings.h>

//#define SERIALIO_RECEIVE

#define DBG_LEV	9
#define SERIALIO_RECEIVE

module SerialIoM
{
	uses interface Boot;
	uses interface Leds;
	uses interface CC2430UartControl;
	uses interface StdControl as UartStdControl;
	uses interface UartStream;
}
implementation
{
	uint8_t m_receive_len;
	uint8_t m_echo_buf;
	uint8_t m_receive_buf[10];
	uint8_t m_send_buf[100];
	
	void showMenu() 
	{
		strcpy(m_send_buf, "\r\n\r\nDemo of Serio I/O\r\n[1] Toggle BLUE LED\r\n[2] Toggle GREEN LED\r\n");
		
		call UartStream.send(m_send_buf, strlen(m_send_buf));
	}
	
	event void Boot.booted()
	{		
		call Leds.BlueLedOn();
		call Leds.YellowLedOn();
		call CC2430UartControl.setBaudRate(9600);
		call UartStdControl.start();
		
		
		#ifdef SERIALIO_RECEIVE
			strcpy(m_send_buf, "DEMO of serial I/O, input  ");
			call UartStream.send(m_send_buf, strlen(m_send_buf));
			call UartStream.receive(m_receive_buf, sizeof(m_receive_buf));
		#else
			showMenu();
		#endif
	}
	
	async event void UartStream.sendDone(uint8_t *buf, uint16_t len, error_t error)
	{
	}
	
	task void showMenuTask()
	{
		showMenu();
	}
	task void lightLED()
	{
		if(m_echo_buf=='1')
		{
			call Leds.BlueLedToggle();  /* ?��????LED?? */
			ADBG(DBG_LEV, "You choose to toggle BLUE LED\r\n");
		}
		else if (m_echo_buf == '2')
		{
			call Leds.YellowLedToggle();/* ?��????LED?? */
			ADBG(DBG_LEV, "You choose to toggle GREEN LED\r\n");
		}
		else
		{
			ADBG(DBG_LEV, "Error Key %c\r\n", m_echo_buf);
			post showMenuTask();
		}
	}
	
	async event void UartStream.receivedByte(uint8_t byte)
	{
		m_echo_buf = byte;
		post lightLED();
	}

	uint8_i compare(unit8_t* input, uint8_t* pattern) {
		uint8_t i;
		for (i = 0; i < 10; i++) {
			if (input[i] != pattern[i]) {
				return 0;
			}
		}
		return 1;
	}
	
	async event void UartStream.receiveDone(uint8_t *buf, uint16_t len, error_t error)
	{
		call UartStream.send(m_receive_buf, sizeof(m_receive_buf));
		
		if (unit8Compare(m_receive_buf, "0123456789")) {
			ADBG(DBG_LEV, "Toggled blue led.\r\n");
			call Leds.BlueLedToggle();
		} else if (unit8Compare(m_receive_buf, "9876543210")) {
			ADBG(DBG_LEV, "Toggled green led.\r\n");
			call Leds.GreenLedToggle();
		} else {
			ADBG(DBG_LEV, "Error Key %c\r\n", m_receive_buf[0]);
		}

		call UartStream.receive(m_receive_buf, sizeof(m_receive_buf));
	}
}

