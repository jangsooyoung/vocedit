<br>
Simple VOC Pascal data 편집기 <br>
============================<br>
<br>
간단한 VOC Pascal Data 편집기<br>
<br>
최대한 간결한 Source로 구성했습니다<br>
프로그램 파일을 1개로 구성하여 개발자가 간단하게 고쳐 쓸 수 있습니다.<br>
<br>
jpg을 읽은후 object 영역을 표시한후 저장 합니다.<br>
xml 파일명은  jpg명 + '.xml'로 기록됩니다.<br>
<br>
![VOCEDIT](./image/VOC.jpg)<br>
<br>
#프로그램 기동<br>
  python3 vocedit.py  jpg_xml_file list <br>
  python3 vocedit_eng.py  jpg_xml_file list # 영문 Version<br>
  - Argument가 최소 1개이상 jpg 파일 이있어야합니다.<br>
 예) python3 vocedit.py *.jpg<br>
<br>
#객체생성<br>
 1. Drag하여 객체 영역 선택<br>
 2. 객체명을 수정한후 저장 <br>
<br>
#객체명 변경<br>
 1. 여러개 객체를 더블클릭<br>
 2. 객체명을 수정한 후 저장<br>
<br>
#객체 Part 생성<br>
 1. 큰 객체 선택 <br>
 2. 큰 객체에 포함된 영영안에서 Drag하여 객체 생성<br>
<br>
#객체선택 조작<br>
	전체선택    : Ctl-A <br>
	전체선택취소 : ESC  <br>
	선택추가  : 왼쪽마우스 더블클릭 <br>
	선택취소  : 오른마우스 클릭 <br>
	선택삭제     : Del    <br>
	Bean자동분석 : Ctrl-P<br>
	<br>
#파일<br>
	파일 읽기 : Ctl-R      <br>
	파일 저장 : Ctl-U      <br>
	이전 파일 : PageUp     <br>
	다음 파일 : PageDown   <br>
