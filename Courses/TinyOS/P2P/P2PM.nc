/*************************************************
*	FUNCTION NAME : P2PM.nc
*	FUNCTION DESCRIPTION : 点对点射频通信
*	FUCNTION DATE :2010/10/18
*	FUNCTION AUTHOR: EMDOOR
**/

/*定义调试级别*/
#define DBG_LEV 1000

module P2PM
{
	uses {
		interface Boot;
		interface StdControl as UartStdControl;
		interface UartStrea0m;
		interface SplitControl as RFControl;
		interface AMSend;
		interface Receive;
		interface AMPacket;
		interface Packet;
		interface Leds;
	}
}
implementation
{
	enum
	{
		MAX_ADDRESS_LEN = 4,
		INPUT_ADDRESS = 0,
		INPUT_DATA = 1,
	};

	message_t m_msg;
	norace uint8_t m_len = 0;
	norace char m_address_str[MAX_ADDRESS_LEN] = {0};
	norace uint8_t m_address_index = 0;
	norace uint8_t m_input_type = 0;
	
	norace uint8_t* received_message;
	norace uint8_t* m;

	/* 显示菜单*/
	task void showMenu()
	{
		if( m_input_type == INPUT_DATA)
		{/*等待输入欲发送的数据*/
			ADBG(DBG_LEV, "\r\n* To Send:\r\n");
		}
		else
		{/*等待输入欲发送的地址*/
			ADBG(DBG_LEV, "\r\n###################################################\r\n* MY NodeId = 0x%x, Group=0x%x, destination ?\r\n",
				ADBG_N(call AMPacket.address()),
				ADBG_N(TOS_IEEE_PANID)
			);
			m_input_type = INPUT_ADDRESS;
			m_address_index = 0;
		}
	}

	uint8_t getLen(uint8_t* string) {
		uint8_t i;
		for (i = 0; string[i] != '\0'; i++);
		return i;
	}
	
	uint8_t compare(uint8_t* text, uint8_t* pattern, uint8_t length) {
		uint8_t i;
		for (i = 0; i < length; i++) {
			if (text[i] != pattern[i]) {
				return 0;
			}
		}
		return 1;
	}
	
	void displayMessage(uint8_t* string) {
		uint8_t len = strlen(string);
		uint8_t i;
		ADBG(DBG_LEV, "\r\nLogger: \r\n");
		for(i=0; i < len;  i++)
		{
			ADBG(DBG_LEV, "%c", string[i]);
		}
	}
	
	/*将从串口输入的地址字符串转化为真实地址*/
	uint16_t getDestAddress()
	{
		uint16_t address = 0;
		uint8_t i = 0;

		if(m_address_index > MAX_ADDRESS_LEN)
		{
			m_address_index = MAX_ADDRESS_LEN -1;
		}

		for ( i=0; i < m_address_index; ++i)
		{
			uint8_t digital = m_address_str[i];
			if(digital >= 'A' && digital <= 'F')
			{
				digital = digital - 'A' + 10;
			}
			else if(digital >= 'a' && digital <= 'f')
			{
				digital = digital - 'a' + 10;
			}
			else if(digital >= '0' && digital <= '9')
			{
				digital = digital - '0';
			}

			address = address*16 +digital;
		}

		return address;
	}

	/* 发送数据*/
	task void sendData()
	{
		uint8_t i;
		uint8_t* payload = call Packet.getPayload(&m_msg, NULL);
		uint16_t address = call AMPacket.address();
		uint16_t dest_address = getDestAddress();

		ADBG( DBG_LEV, "\r\n\r\n* Sending ... from [%d], to [%d], len=[%d]\r\n",
			ADBG_N(address),
			ADBG_N(dest_address),
			ADBG_N(m_len)
		);
	
		call AMSend.send(dest_address, &m_msg, m_len);

		call Leds.BlueLedToggle();
	}

	/*发送完处理*/
	event void AMSend.sendDone(message_t* msg, error_t success)
	{
		ADBG(DBG_LEV, "* Sent%s!\r\n", (success == SUCCESS) ? "OK" : "FAIL");
		m_len = 0;

		m_input_type = INPUT_ADDRESS;

		
		post showMenu();
	}

	/*从串口接收数据*/
	async event void UartStream.receivedByte(uint8_t c)
	{
		if(c != '\r')
		{		
			if (m_input_type == INPUT_DATA)
			{/*输入数据*/
				uint8_t* payload = (uint8_t*)call Packet.getPayload(&m_msg, NULL);
				if(m_len >= call Packet.maxPayloadLength())
				{
					return;
				}

				payload[m_len++] = c;
				ADBG(DBG_LEV, "%c", c);

				if(m_len < call Packet.maxPayloadLength())
				{
					return;
				}
			}
			else
			{/*输入地址*/
				if(m_address_index < MAX_ADDRESS_LEN)
				{
					m_address_str[m_address_index++] = c;
					ADBG(DBG_LEV, "%c", c);
				}

				if(m_address_index < MAX_ADDRESS_LEN)
				{
					return;
				}
			}
		}

		/*按下回车键或者到达最大长度，则处理*/
		if(m_input_type == INPUT_DATA)
		{
			post sendData();
		}
		else
		{
			/*地址处理完毕，准备输入数据*/
			m_input_type = INPUT_DATA;
			post showMenu();
		}
	}
				
	/* 节点启动完毕*/
	event void Boot.booted()
	{
		/*开启射频*/
		call RFControl.start();

		/*开启串口通信*/
		call UartStdControl.start();

		call Leds.YellowLedOff();
		call Leds.BlueLedOff();

		ADBG(DBG_LEV, "\r\n###############################################\r\n");
		ADBG(DBG_LEV, "   [P2PDEMO] My Address = 0x%x, Group = 0x%x\r\n", ADBG_N(call AMPacket.address()), ADBG_N(TOS_IEEE_PANID));
		ADBG(DBG_LEV, "###############################################\r\n");

		m_input_type = INPUT_ADDRESS;
		post showMenu();
	}

	/** 实现接口RFControl 接口中的事件*/
	event void RFControl.startDone(error_t result)
	{
	}

	event void RFControl.stopDone(error_t result)
	{
	}

	/** 实现接口UartStream 接口中的事件*/
	async event void UartStream.sendDone(uint8_t* buf, uint16_t len, error_t error)
	{
	}

	async event void UartStream.receiveDone(uint8_t* buf, uint16_t len, error_t error)
	{
	}

	
	
	/*射频接收数据*/
	event message_t* Receive.receive(message_t* msg, void* payload, uint8_t len)
	{
		uint8_t i;
		received_message = (uint8_t*)payload;

		ADBG(DBG_LEV, "\r\n*Receive, len = [%d], DATA:\r\n", ADBG_N(len));
		
		for(i = 0; i < len; i++)
		{
			ADBG(DBG_LEV, "%c", ((uint8_t*)payload)[i]);
		}
		ADBG(DBG_LEV, "\r\n");
		
		call Leds.YellowLedToggle();

		m_input_type = INPUT_ADDRESS;

		post showMenu();

		length1 = getLen(received_message);
		length2 = getLen(sent_message);
		if (length1 == length2 && compare(received_message, sent_message, length1)) {
			ADBG(DBG_LEV, "Received message matches sent message.\r\n");
			call Leds.RedLedToggle();
		} else {
			ADBG(DBG_LEV, "Received message does not match sent message.\r\n");
		}
	}
}

