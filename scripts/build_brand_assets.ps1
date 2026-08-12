param([string]$Root = (Split-Path -Parent $PSScriptRoot))

Add-Type -AssemblyName System.Drawing

function New-Canvas([int]$Width, [int]$Height, [string]$Path, [scriptblock]$Paint) {
  $bitmap = [Drawing.Bitmap]::new($Width, $Height, [Drawing.Imaging.PixelFormat]::Format24bppRgb)
  $graphics = [Drawing.Graphics]::FromImage($bitmap)
  $graphics.SmoothingMode = [Drawing.Drawing2D.SmoothingMode]::AntiAlias
  $graphics.TextRenderingHint = [Drawing.Text.TextRenderingHint]::AntiAliasGridFit
  & $Paint $graphics $Width $Height
  $directory = Split-Path -Parent $Path
  [IO.Directory]::CreateDirectory($directory) | Out-Null
  $bitmap.Save($Path, [Drawing.Imaging.ImageFormat]::Png)
  $graphics.Dispose()
  $bitmap.Dispose()
}

function Brush([string]$Hex) { [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml($Hex)) }
function Pen([string]$Hex, [float]$Width = 2) { [Drawing.Pen]::new([Drawing.ColorTranslator]::FromHtml($Hex), $Width) }
function Font([float]$Size, [Drawing.FontStyle]$Style = [Drawing.FontStyle]::Regular, [string]$Family = 'Segoe UI') { [Drawing.Font]::new($Family, $Size, $Style, [Drawing.GraphicsUnit]::Pixel) }
function Line($g, $pen, [float]$x1, [float]$y1, [float]$x2, [float]$y2) { $g.DrawLine($pen, $x1, $y1, $x2, $y2) }
function Node($g, [float]$x, [float]$y, [float]$r, [string]$fill, [string]$stroke) { $b=Brush $fill; $p=Pen $stroke 3; $g.FillEllipse($b,$x-$r,$y-$r,$r*2,$r*2); $g.DrawEllipse($p,$x-$r,$y-$r,$r*2,$r*2); $b.Dispose();$p.Dispose() }
function Text($g,[string]$value,[float]$x,[float]$y,[float]$size,[string]$color,[Drawing.FontStyle]$style=[Drawing.FontStyle]::Regular,[string]$family='Segoe UI'){ $f=Font $size $style $family; $b=Brush $color; $g.DrawString($value,$f,$b,$x,$y);$f.Dispose();$b.Dispose() }

$readme = Join-Path $Root 'assets\signal-loom-readme-hero.png'
New-Canvas 1600 720 $readme {
  param($g,$w,$h)
  $g.Clear([Drawing.ColorTranslator]::FromHtml('#07141C'))
  $grid=Pen '#123747' 1
  for($x=0;$x -lt $w;$x+=80){Line $g $grid $x 0 $x $h};for($y=0;$y -lt $h;$y+=80){Line $g $grid 0 $y $w $y};$grid.Dispose()
  Text $g 'SIGNAL LOOM' 88 64 28 '#F4B6DD' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'Evidence becomes a story without losing its threads.' 88 112 48 '#F5FAFC' ([Drawing.FontStyle]::Bold)
  Text $g 'SOURCE' 104 260 18 '#9DDFF0' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'CLAIM' 414 260 18 '#F0C36A' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'STORY' 724 260 18 '#F29B91' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'FORM' 1034 260 18 '#BFAFF5' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'REVIEW' 1322 260 18 '#98DFC1' ([Drawing.FontStyle]::Bold) 'Consolas'
  $xs=@(140,450,760,1070,1370);$colors=@('#48CBE8','#E0AF5C','#EF6D64','#9888E6','#74C6A4')
  for($i=0;$i -lt 4;$i++){ $p=Pen $colors[$i] 7; Line $g $p ($xs[$i]+34) 348 ($xs[$i+1]-34) 348; $p.Dispose() }
  for($i=0;$i -lt 5;$i++){Node $g $xs[$i] 348 28 '#07141C' $colors[$i]}
  $small=Pen '#426473' 2
  foreach($offset in @(-42,-21,21,42)){ Line $g $small 96 (348+$offset) 112 (348+$offset); Line $g $small 1398 (348+$offset) 1414 (348+$offset) };$small.Dispose()
  Text $g 'A governed causal spine' 88 468 28 '#D7E6EB' ([Drawing.FontStyle]::Bold)
  Text $g 'Supplied sources  |  explicit status  |  earned representation  |  human authority' 88 516 22 '#9BB4BF'
  Text $g 'Loomfile: resumable project state, not an export graveyard.' 88 586 20 '#74C6A4' ([Drawing.FontStyle]::Bold) 'Consolas'
}

$pages = Join-Path $Root 'docs\assets\signal-loom-pages-hero.png'
New-Canvas 1200 800 $pages {
  param($g,$w,$h)
  $g.Clear([Drawing.ColorTranslator]::FromHtml('#F2EEE5'))
  $dark=Brush '#102733';$g.FillRectangle($dark,0,0,360,$h);$dark.Dispose()
  Text $g 'THE LOOMFILE' 56 62 20 '#F4B6DD' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'One studio.' 56 112 48 '#FFFFFF' ([Drawing.FontStyle]::Bold)
  Text $g 'Seven stages.' 56 170 48 '#FFFFFF' ([Drawing.FontStyle]::Bold)
  Text $g 'No severed' 56 228 48 '#FFFFFF' ([Drawing.FontStyle]::Bold)
  Text $g 'provenance.' 56 286 48 '#FFFFFF' ([Drawing.FontStyle]::Bold)
  Text $g 'ORIENT' 58 405 18 '#48CBE8' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'SHAPE' 58 445 18 '#E0AF5C' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'PLAN' 58 485 18 '#EF6D64' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'BUILD' 58 525 18 '#9888E6' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'FINISH' 58 565 18 '#74C6A4' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'DISTRIBUTE' 58 605 18 '#D470BA' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'VERIFY' 58 645 18 '#F5FAFC' ([Drawing.FontStyle]::Bold) 'Consolas'
  $card=Brush '#FFFFFF';$outline=Pen '#CFD7D7' 2
  $cards=@(@(420,72,320,174),@(780,72,360,174),@(420,286,720,174),@(420,500,320,220),@(780,500,360,220))
  foreach($c in $cards){$g.FillRectangle($card,$c[0],$c[1],$c[2],$c[3]);$g.DrawRectangle($outline,$c[0],$c[1],$c[2],$c[3])}
  Text $g 'sources/' 450 98 20 '#2F8196' ([Drawing.FontStyle]::Bold) 'Consolas';Text $g 'originals + hashes' 450 140 24 '#19323C' ([Drawing.FontStyle]::Bold);Text $g 'authority + freshness' 450 182 18 '#64777E'
  Text $g 'claims.jsonl' 810 98 20 '#9B6A25' ([Drawing.FontStyle]::Bold) 'Consolas';Text $g 'sourced | inferred' 810 140 24 '#19323C' ([Drawing.FontStyle]::Bold);Text $g 'missing | stale | disputed' 810 182 18 '#64777E'
  Text $g 'story spine' 450 312 20 '#AC5149' ([Drawing.FontStyle]::Bold) 'Consolas';Text $g 'Pulse  ->  tension  ->  turn  ->  payoff' 450 358 30 '#19323C' ([Drawing.FontStyle]::Bold);Text $g 'Five to nine beats. Every beat carries evidence links.' 450 410 19 '#64777E'
  Text $g 'visual plan' 450 528 20 '#6D5DB5' ([Drawing.FontStyle]::Bold) 'Consolas';Text $g 'PROSE' 450 580 17 '#19323C' ([Drawing.FontStyle]::Bold);Text $g 'DIAGRAM' 450 614 17 '#19323C' ([Drawing.FontStyle]::Bold);Text $g 'CHART' 450 648 17 '#19323C' ([Drawing.FontStyle]::Bold);Text $g 'INTERACTION' 450 682 17 '#19323C' ([Drawing.FontStyle]::Bold)
  Text $g 'review/' 810 528 20 '#2C8869' ([Drawing.FontStyle]::Bold) 'Consolas';Text $g 'static checks' 810 580 22 '#19323C' ([Drawing.FontStyle]::Bold);Text $g 'human review' 810 620 22 '#19323C' ([Drawing.FontStyle]::Bold);Text $g 'manual publication' 810 660 22 '#19323C' ([Drawing.FontStyle]::Bold)
  $card.Dispose();$outline.Dispose()
}

$social = Join-Path $Root 'docs\assets\signal-loom-social-card.png'
New-Canvas 1200 630 $social {
  param($g,$w,$h)
  $g.Clear([Drawing.ColorTranslator]::FromHtml('#06131C'))
  $left=Brush '#48CBE8';$g.FillRectangle($left,0,0,24,$h);$left.Dispose()
  $gold=Brush '#E0AF5C';$g.FillRectangle($gold,24,0,12,$h);$gold.Dispose()
  Text $g 'SIGNAL LOOM' 88 88 72 '#FFFFFF' ([Drawing.FontStyle]::Bold)
  Text $g 'Evidence-to-visual story production' 92 186 31 '#F4B6DD' ([Drawing.FontStyle]::Bold)
  Text $g 'SOURCE' 94 332 17 '#48CBE8' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'CLAIM' 310 332 17 '#E0AF5C' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'STORY' 526 332 17 '#EF6D64' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'FORM' 742 332 17 '#9888E6' ([Drawing.FontStyle]::Bold) 'Consolas'
  Text $g 'REVIEW' 944 332 17 '#74C6A4' ([Drawing.FontStyle]::Bold) 'Consolas'
  $xs=@(126,342,558,774,986);$colors=@('#48CBE8','#E0AF5C','#EF6D64','#9888E6','#74C6A4')
  for($i=0;$i -lt 4;$i++){ $p=Pen $colors[$i] 5;Line $g $p ($xs[$i]+19) 405 ($xs[$i+1]-19) 405;$p.Dispose() }
  for($i=0;$i -lt 5;$i++){Node $g $xs[$i] 405 17 '#06131C' $colors[$i]}
  Text $g 'Shape the story. Keep every thread inspectable.' 92 500 28 '#D7E6EB'
  Text $g 'Manual publication  |  resumable Loomfile  |  source-bound claims' 92 552 18 '#8EA9B5' ([Drawing.FontStyle]::Bold) 'Consolas'
}

Write-Output "Built:`n$readme`n$pages`n$social"