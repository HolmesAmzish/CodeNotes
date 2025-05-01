COMPONENT = P2PC

##########################

#使用串口调试模块
PFLAGS += -DUART_DEBUG

PFLAGS += -DUSE_MODULE_LED

#调试级别
PFLAGS += -DADBG_LEVEL=1000

#射频，不限制地址
PFLAGS += -DNO_RADIO_ADDRESS_REQ

#使用硬件ACK
PFLAGS += -DCC2420_HW_ACKNOWLEDGEMENTS

#链路层使用重发机制
PFLAGS += -DPACKET_LINK


#使用CC2420射频协议栈
USE_CC2420_STACK = 1

######################

include $(MAKERULES)

