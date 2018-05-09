import java.net.*;
import java.util.*;

public class getIP{
    public static void main(String[] args){
        try{
            Scanner scn = new Scanner(System.in);
            
            String ip_add = scn.next();
            InetAddress addr = InetAddress.getByName(ip_add);
            System.out.println(addr);

            byte[] ip = addr.getAddress();
            for(byte i: ip){
                int unsignedByte = i < 0? i + 256 : i;
                System.out.println(unsignedByte);
            }
            
            scn.close();

        }catch(UnknownHostException e){
            System.out.println("Unable to connect");
        }
    }
}