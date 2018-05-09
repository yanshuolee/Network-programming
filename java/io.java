import java.util.*;

public class io{
    public static void main(String[] args) {
        Scanner scn = new Scanner(System.in);
        System.out.println("height & weight");
        float h, w;
        h = scn.nextFloat();
        w = scn.nextFloat();
        float bmi;
        bmi = w/h/h;
        System.out.println("BMI = " + bmi);
        scn.close();
    }
}