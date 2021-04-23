<html>
<head>

<?php
if (isset($_POST['ron']))   // Red on
{
exec('sudo python3 /var/www/cpin7l.py');
}
if (isset($_POST['roff']))  //  Red Off
{
exec('sudo python3 /var/www/cpin7h.py');
}
if (isset($_POST['gon']))   // Green On
{
exec('sudo python3 /var/www/cpin5l.py');
}
if (isset($_POST['goff']))  // Green Off
{
exec('sudo python3 /var/www/cpin5h.py');
}
if (isset($_POST['bon']))   // Blue On
{
exec('sudo python3 /var/www/cpin3l.py');
}
if (isset($_POST['boff']))  // Blue Off
{
exec('sudo python3 /var/www/cpin3h.py');
}
?>

  <title>SMlab8-APACHE server for Web of Things  </title>
</head>
<body bgcolor="silver">
<center>
<table witdh="400" border="1" bgcolor="silver" bordercolor="blue">
<td>

<font face="verdana" color="navy">
<center>
"Gh.Asachi" Technical University of  Iasi - Romania 
<br><br>
</font>


<center>  <Font face="impact" color='navy' font size="4">
SMlab8 - Apache Server for Web of Things   </font><br>
<font color="white" face ="arial" size="2">
Light  the world from anywhere</font>
</font><br><br>
<img src="/imag/imag1.jpg" width="250" height="150"> </center>
<br>

<center>
<form method="post">
  <table
 style="width: 50%; text-align: left; margin-left: auto; margin-right: auto;"
 border="1" cellpadding="2" cellspacing="2">
      <tr>
        <td style="text-align: center;"><button name="ron"><font face="impact" color="red">RED ON</button></td></font>
        <td style="text-align: center;"><button name="roff"><font face="impact" color="red">RED OFF </button></td> </font>
      </tr>
      <tr>
        <td  style="text-align: center;"><button name="gon"><font face="impact" color="green">GREEN ON</button></td></font>
        <td  style="text-align: center;"><button name="goff"><font face="impact" color="green">GREEN OFF</button></td></font>
      </tr>
      <tr>
        <td  style="text-align: center;"><button name="bon"><font face="impact" color="blue">BLUE ON</button></td></font>
        <td  style="text-align: center;"><button name="boff"><font face="impact" color="blue">BLUE OFF</button></td></font>
      </tr>
    </tbody>
  </table>

</form>



<center>
<br> <font face="arial" color="navy">
&copy 2021 Automation and Computer Engineering Faculty
 <br>
</td>
</table>

</body>
</html>

