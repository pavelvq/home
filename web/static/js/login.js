var sFadeStartColor = "#DDDDDD";
var sFadeFinishColor = "#000000";

//разбиваем RGB-триплеты на красный, зеленый и синий в виде массива
var aRGBStart = sFadeStartColor.replace("#","").match(/.{2}/g); 
var aRGBFinish = sFadeFinishColor.replace("#","").match(/.{2}/g);

var s2FadeStartColor = "#000000";
var s2FadeFinishColor = "#DDDDDD";

//разбиваем RGB-триплеты на красный, зеленый и синий в виде массива
var a2RGBStart = s2FadeStartColor.replace("#","").match(/.{2}/g);
var a2RGBFinish = s2FadeFinishColor.replace("#","").match(/.{2}/g);

var t=30; //t - время задержки в миллисекундах 
/* n - количество промежуточных цветов, включая конечный 
(т.е. между начальным и конечным цветами будет n-1 цвет) */
var n = 100;

var i = 0; //индекс текущего промежуточного цвета 
var l = 0;

function getFadeMiddleColor() 
{
  /*процент содержания конечного цвета в текущем промежуточном цвете;
  изменяется от 0 (не включая 0) до 1 (1 = 100%)*/
  var finishPercent = i/n;
  /*процент содержания начального цвета в текущем промежуточном цвете;
  изменяется от 1 до 0 (1 = 100%) */
  var startPercent = 1 - finishPercent;
  
  var R,G,B;
  
  //вычисляем значения красного, зеленого, синего промежуточного цвета
  R = Math.floor( ('0x'+aRGBStart[0]) * startPercent + ('0x'+aRGBFinish[0]) * finishPercent );
  G = Math.floor( ('0x'+aRGBStart[1]) * startPercent + ('0x'+aRGBFinish[1]) * finishPercent );
  B = Math.floor( ('0x'+aRGBStart[2]) * startPercent + ('0x'+aRGBFinish[2]) * finishPercent );
  
  return 'rgb('+R+ ',' + G + ',' + B +')'; 
}

function getFadeMiddleColor2()
{
  /*процент содержания конечного цвета в текущем промежуточном цвете;
  изменяется от 0 (не включая 0) до 1 (1 = 100%)*/
  var finishPercent = i/n;
  /*процент содержания начального цвета в текущем промежуточном цвете;
  изменяется от 1 до 0 (1 = 100%) */
  var startPercent = 1 - finishPercent;

  var R,G,B;

  //вычисляем значения красного, зеленого, синего промежуточного цвета
  R = Math.floor( ('0x'+a2RGBStart[0]) * startPercent + ('0x'+a2RGBFinish[0]) * finishPercent );
  G = Math.floor( ('0x'+a2RGBStart[1]) * startPercent + ('0x'+a2RGBFinish[1]) * finishPercent );
  B = Math.floor( ('0x'+a2RGBStart[2]) * startPercent + ('0x'+a2RGBFinish[2]) * finishPercent );

  return 'rgb('+R+ ',' + G + ',' + B +')';
}

function fade()
{
  if (l == 0) {
    i++;
  }
  else {
    i = i - 1;
  }
  
  document.getElementById('backg').style.backgroundColor = getFadeMiddleColor();
  document.getElementById('lform').style.backgroundColor = getFadeMiddleColor2();
  document.getElementById('l').style.color = getFadeMiddleColor();
  document.getElementById('p').style.color = getFadeMiddleColor();
  
  if (l == 0) {
    if ( i < n ) {
        setTimeout(fade, t); 
    }  
    else {
        l = 1
        setTimeout(fade, t); 
    }
  }
  else {
    if ( i > 0 ) {
        setTimeout(fade, t); 
    }  
    else {
        l = 0
        setTimeout(fade, t); 
    }
  }
  console.log(i, l)
} 

fade();
