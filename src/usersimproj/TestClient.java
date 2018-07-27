package usersimproj;

import java.net.*;

public class TestClient
{
    public DatagramSocket m_client_sock;
    public InetAddress m_serv_addr;

    public TestClient()
    {
        try
        {
            m_serv_addr = InetAddress.getLocalHost();
            m_client_sock = new DatagramSocket(8306, m_serv_addr);
        }
        catch (Exception e)
        {
            System.out.println(e.toString());
        }
    }

    public static void main(String[] argv)
    {
        TestClient tc = new TestClient();
        byte[] buf = new byte[256];

        while(true)
        {
            try
            {
                System.out.println("Client starts...");
                //String send_str = "This is a client!";
                String send_str = "oo" + "#" + "06387980n+06388579n" + "#" + "03588414n";
                byte[] send_buf = send_str.getBytes();
                DatagramPacket send_pack = new DatagramPacket(send_buf, send_buf.length, tc.m_serv_addr, 8607);
                System.out.println("Client sends out a package!");
                tc.m_client_sock.send(send_pack);

                DatagramPacket recv_pack = new DatagramPacket(buf, buf.length);
                tc.m_client_sock.receive(recv_pack);
                System.out.println("Client received a package!");
                String recv_str = new String(recv_pack.getData(), 0, recv_pack.getLength());
                System.out.println(recv_str);
                System.out.println("Client terminates!");
            }
            catch(Exception e)
            {
                System.out.println(e.toString());
            }
        }
    }
}
