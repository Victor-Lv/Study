##网络安全之SSL协议和IPSec协议：  
SSL(Secure Socket Layer)协议位于TCP/IP协议与各种应用层协议之间，为数据通讯提供安全支持。SSL协议可分为两层： SSL记录协议（SSL Record Protocol）：它建立在可靠的传输协议（如TCP）之上，为高层协议提供数据封装、压缩、加密等基本功能的支持。 SSL握手协议（SSL Handshake Protocol）：它建立在SSL记录协议之上，用于在实际的数据传输开始前，通讯双方进行身份认证、协商加密算法、交换加密密钥等。  
SSL架构图：  
![SSL架构图](https://github.com/Victor-Lv/Study/blob/master/network_security/image/SSL_framework.jpg)  

