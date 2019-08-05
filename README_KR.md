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
![VOCEDIT](./img/VOC.jpg)<br>
<br>
#프로그램 기동<br>
  python3 vocedit.py  ]jpg_xml_file list] <br>
  python3 vocedit_eng.py  ]jpg_xml_file list] # 영문 Version<br>
 예) python3 vocedit.py [ image_file ] <br>
<br>
#객체생성<br>
 1. Drag하여 객체 영역 선택<br>
 2. 객체명을 수정한후 저장[Enter]<br>
<br>
#객체명 변경<br>
 1. 여러개 객체를 더블클릭<br>
 2. 객체명을 수정한 후 저장[Enter]<br>
<br>
#객체 Part 생성<br>
 1. 큰 객체 선택 <br>
 2. 큰 객체에 포함된 영영안에서 Drag하여 객체 생성<br>
#객체명 이동<br>
 l. 객체선택후 화살표<br>
#객체명 크기변경<br>
 1. 객체선택후 Cntl+화살표<br>
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
<br>
# Image 분할후 객체명  정리하기 <br>
  객체명 분류가 잘되었는지 검증하는 방법 <br>
<br>
 1. python3 vocsplit.py dest_dir img_List<br>
    img_list에 있는 voc xml읙 객체를 객체명으로된 sub directory별로 분류하여 저장한다.<br>
<br>
 2.  dest_dir에 생성됨 이미지를 재배치 한다<br>
     이대 "del"이라는 sub_directory로 옴겨진 객체 image는 객체 삭제 대상이다 <br>
     생성된 객체 파일명을 수정하면 안된다 <br>
     파일명을 수정하면 XML을 수정할수 있다 <br>
<br>
 3. python3 vocrenameobk.py dest_dir img_List<br>
    vocsplit.py로  dest_dir 별로 분할된 Image목록을 읽어 XML의 객체명을 수정한다.<br>
