# -*- coding: utf-8 -*-
from django.shortcuts import render
from config import settings
from kakaocert import RequestCMS, KakaocertService, RequestVerifyAuth, KakaocertException, RequestESign


# config/settings.py 인증정보(LinkID, SecretKey)를 이용해
# KakaocertService 객체 인스턴스 생성
kakaocertService = KakaocertService(settings.LinkID, settings.SecretKey)

# 인증토큰 IP제한기능 사용여부, 권장(True)
kakaocertService.IPRestrictOnOff = settings.IPRestrictOnOff

# 카카오써트 API 서비스 고정 IP 사용여부, True-사용, False-미사용, 기본값(False)
kakaocertService.UseStaticIP = settings.UseStaticIP

# 로컬시스템 시간 사용여부 True-사용, False-미사용, 기본값(True)
kakaocertService.UseLocalTimeYN = settings.UseLocalTimeYN

def reqeustESignhandler(request):
    """
    전자서명을 요청합니다.
    - https://www.kakaocert.com/docs/ESign/API/python#RequestESign
    """
    try:

        # Kakaocert 이용기관코드, Kakaocert 파트너 사이트에서 확인
        clientCode = '020040000001'

        # AppToApp 인증 여부
        # True-App To App 방식, False-Talk Message 방식
        appUseYN = False;

        # 전자서명 요청정보 객체
        requestObj = RequestESign(

            # 고객센터 전화번호, 카카오톡 인증메시지 중 "고객센터" 항목에 표시
            CallCenterNum = '1600-8536',

            # 고객센터명, 카카오톡 인증메시지 중 "고객센터명" 항목에 표시
            CallCenterName = '테스트',

            # 인증요청 만료시간(초), 최대값 1000, 인증요청 만료시간(초) 내에 미인증시 만료 상태로 처리됨
            Expires_in = 60,

            # 수신자 생년월일, 형식 : YYYYMMDD
            ReceiverBirthDay = '19700101',

            # 수신자 휴대폰번호
            ReceiverHP = '010111222',

            # 수신자 성명
            ReceiverName = '홍길동',

            # 별칭코드, 이용기관이 생성한 별칭코드 (파트너 사이트에서 확인가능)
            # 카카오톡 인증메시지 중 "요청기관" 항목에 표시
            # 별칭코드 미 기재시 이용기관의 이용기관명이 "요청기관" 항목에 표시
            SubClientID = '',

            # 인증요청 메시지 부가내용, 카카오톡 인증메시지 중 상단에 표시
            TMSMessage = 'TMSMessage0423',

            # 인증요청 메시지 제목, 카카오톡 인증메시지 중 "요청구분" 항목에 표시
            TMSTitle = 'TMSTitle 0423',

            # 은행계좌 실명확인 생략여부
            # true : 은행계좌 실명확인 절차를 생략
            # false : 은행계좌 실명확인 절차를 진행
            # 카카오톡 인증메시지를 수신한 사용자가 카카오인증 비회원일 경우, 카카오인증 회원등록 절차를 거쳐 은행계좌 실명확인 절차를 밟은 다음 전자서명 가능
            isAllowSimpleRegistYN = False,

            # 수신자 실명확인 여부
            # true : 카카오페이가 본인인증을 통해 확보한 사용자 실명과 ReceiverName 값을 비교
            # false : 카카오페이가 본인인증을 통해 확보한 사용자 실명과 RecevierName 값을 비교하지 않음.
            isVerifyNameYN = True,

            # 전자서명할 토큰 원문
            Token = 'Token Value 2345',

            # PayLoad, 이용기관이 생성한 payload(메모) 값
            PayLoad = 'Payload123'

        )

        response = kakaocertService.requestESign(clientCode, requestObj, appUseYN)

        return render(request, 'responseESign.html', {'receiptId': response.receiptId, 'tx_id': response.tx_id})
    except KakaocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

def getESignStatehandler(request):
    """
    전자서명 요청시 반환된 접수아이디를 통해 서명 상태를 확인합니다.
    - https://www.kakaocert.com/docs/ESign/API/python#GetESignState
    """
    try:
        # Kakaocert 이용기관코드, Kakaocert 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '022052511005100001'

        response = kakaocertService.getESignState(clientCode, receiptId)

        return render(request, 'getESignState.html', {'response': response})
    except KakaocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})


def verifyESignhandler(request):
    """
    전자서명 요청시 반환된 접수아이디를 통해 서명을 검증합니다.
    - 서명검증시 전자서명 데이터 전문(signedData)이 반환됩니다.
    - 카카오페이 서비스 운영정책에 따라 검증 API는 1회만 호출할 수 있습니다. 재시도시 오류처리됩니다.
    - https://www.kakaocert.com/docs/ESign/API/python#VerifyESign
    """
    try:
        # Kakaocert 이용기관코드, Kakaocert 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '022050912183600001'

        # AppToApp 인증시, 앱스킴 성공처리시 반환되는 서명값(iOS-sig, Android-signature)
        # Talk Message 인증시 None 기재
        signature = None

        response = kakaocertService.verifyESign(clientCode, receiptId, signature)

        return render(request, 'responseVerify.html', {'response': response})
    except KakaocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})


def reqeustVerifyAuthhandler(request):
    """
    본인인증 전자서명을 요청합니다.
    - 본인인증 서비스에서 이용기관이 생성하는 Token은 사용자가 전자서명할 원문이 됩니다. 이는 보안을 위해 1회용으로 생성해야 합니다.
    - 사용자는 이용기관이 생성한 1회용 토큰을 서명하고, 이용기관은 그 서명값을 검증함으로써 사용자에 대한 인증의 역할을 수행하게 됩니다.
    - https://www.kakaocert.com/docs/verifyAuth/API/python#RequestVerifyAuth
    """
    try:

        # Kakaocert 이용기관코드, Kakaocert 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 본인인증 요청정보 객체
        requestObj = RequestVerifyAuth(

            # 고객센터 전화번호, 카카오톡 인증메시지 중 "고객센터" 항목에 표시
            CallCenterNum = '1600-8536',

            # 고객센터명, 카카오톡 인증메시지 중 "고객센터명" 항목에 표시
            CallCenterName = '테스트',

            # 인증요청 만료시간(초), 최대값 1000, 인증요청 만료시간(초) 내에 미인증시 만료 상태로 처리됨
            Expires_in = 60,

            # 수신자 생년월일, 형식 : YYYYMMDD
            ReceiverBirthDay = '19700101',

            # 수신자 휴대폰번호
            ReceiverHP = '010111222',

            # 수신자 성명
            ReceiverName = '홍길동',

            # 별칭코드, 이용기관이 생성한 별칭코드 (파트너 사이트에서 확인가능)
            # 카카오톡 인증메시지 중 "요청기관" 항목에 표시
            # 별칭코드 미 기재시 이용기관의 이용기관명이 "요청기관" 항목에 표시
            SubClientID = '',

            # 인증요청 메시지 부가내용, 카카오톡 인증메시지 중 상단에 표시
            TMSMessage = 'TMSMessage0423',

            # 인증요청 메시지 제목, 카카오톡 인증메시지 중 "요청구분" 항목에 표시
            TMSTitle = 'TMSTitle 0423',

            # 은행계좌 실명확인 생략여부
            # true : 은행계좌 실명확인 절차를 생략
            # false : 은행계좌 실명확인 절차를 진행
            # 카카오톡 인증메시지를 수신한 사용자가 카카오인증 비회원일 경우, 카카오인증 회원등록 절차를 거쳐 은행계좌 실명확인 절차를 밟은 다음 전자서명 가능
            isAllowSimpleRegistYN = False,

            # 수신자 실명확인 여부
            # true : 카카오페이가 본인인증을 통해 확보한 사용자 실명과 ReceiverName 값을 비교
            # false : 카카오페이가 본인인증을 통해 확보한 사용자 실명과 RecevierName 값을 비교하지 않음.
            isVerifyNameYN = True,

            # 전자서명할 토큰 원문
            Token = 'Token Value 2345',

            # PayLoad, 이용기관이 생성한 payload(메모) 값
            PayLoad = 'Payload123',
        )

        result = kakaocertService.requestVerifyAuth(clientCode, requestObj)

        return render(request, 'response.html', {'receiptId': result.receiptId})
    except KakaocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})


def getVerifyAuthStatehandler(request):
    """
    본인인증 요청시 반환된 접수아이디를 통해 서명 상태를 확인합니다.
    - https://www.kakaocert.com/docs/verifyAuth/API/python#GetVerifyAuthState
    """
    try:
        # Kakaocert 이용기관코드, Kakaocert 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 본인인증 요청시 반환받은 접수아이디
        receiptId = '022050912192100001'

        response = kakaocertService.getVerifyAuthState(clientCode, receiptId)

        return render(request, 'getVerifyAuthState.html', {'response': response})
    except KakaocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

def verifyAuthhandler(request):
    """
    본인인증 요청시 반환된 접수아이디를 통해 본인인증 서명을 검증합니다.
    - 서명검증시 전자서명 데이터 전문(signedData)이 반환됩니다.
    - 본인인증 요청시 작성한 Token과 서명 검증시 반환되는 signedData의 동일여부를 확인하여 본인인증 검증을 완료합니다.
    - 카카오페이 서비스 운영정책에 따라 검증 API는 1회만 호출할 수 있습니다. 재시도시 오류처리됩니다.
    - https://www.kakaocert.com/docs/verifyAuth/API/python#F-VerifyAuth
    """
    try:
        # Kakaocert 이용기관코드, Kakaocert 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 본인인증 요청시 반환받은 접수아이디
        receiptId = '022050912192100001'

        response = kakaocertService.verifyAuth(clientCode, receiptId)

        return render(request, 'responseVerify.html', {'response': response})
    except KakaocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

def reqeustCMShandler(request):
    """
    자동이체 출금동의 전자서명을 요청합니다.
    - 해당 서비스는 전자서명을 하는 당사자와 출금계좌의 예금주가 동일한 경우에만 사용이 가능합니다.
    - 전자서명 당사자와 출금계좌의 예금주가 동일인임을 체크하는 의무는 이용기관에 있습니다.
    - 금융결제원에 증빙자료(전자서명 데이터) 제출은 이용기관 측 에서 진행해야 합니다.
    - https://www.kakaocert.com/docs/CMS/API/python#RequestCMS
    """
    try:

        # Kakaocert 이용기관코드, Kakaocert 파트너 사이트에서 확인
        clientCode = '020040000001';

        # AppToApp 인증 여부
        # True-App To App 방식, False-Talk Message 방식
        appUseYN = False;

        # 자동이체 출금동의 요청정보 객체
        requestObj = RequestCMS(

            # 고객센터 전화번호, 카카오톡 인증메시지 중 "고객센터" 항목에 표시
            CallCenterNum = '1600-8536',

            # 고객센터명, 카카오톡 인증메시지 중 "고객센터명" 항목에 표시
            CallCenterName = '테스트',

            # 인증요청 만료시간(초), 최대값 1000, 인증요청 만료시간(초) 내에 미인증시 만료 상태로 처리됨
            Expires_in = 60,

            # 수신자 생년월일, 형식 : YYYYMMDD
            ReceiverBirthDay = '19700101',

            # 수신자 휴대폰번호
            ReceiverHP = '010111222',

            # 수신자 성명
            ReceiverName = '홍길동',

            # 예금주명
            BankAccountName = '예금주명',

            # 계좌번호, 이용기관은 사용자가 식별가능한 범위내에서 계좌번호의 일부를 마스킹 처리할 수 있음 (예시) 371-02-6***85
            BankAccountNum = '9-4324-5**7-58',

            # 참가기관 코드
            BankCode = '004',

            # 납부자번호, 이용기관에서 부여한 고객식별번호
            ClientUserID = 'clientUserID-0423-01',

            # 별칭코드, 이용기관이 생성한 별칭코드 (파트너 사이트에서 확인가능)
            # 카카오톡 인증메시지 중 "요청기관" 항목에 표시
            # 별칭코드 미 기재시 이용기관의 이용기관명이 "요청기관" 항목에 표시
            SubClientID = '020040000001',

            # 인증요청 메시지 부가내용, 카카오톡 인증메시지 중 상단에 표시
            TMSMessage = 'TMSMessage0423',

            # 인증요청 메시지 제목, 카카오톡 인증메시지 중 "요청구분" 항목에 표시
            TMSTitle = 'TMSTitle 0423',

            # 은행계좌 실명확인 생략여부
            # true : 은행계좌 실명확인 절차를 생략
            # false : 은행계좌 실명확인 절차를 진행
            # 카카오톡 인증메시지를 수신한 사용자가 카카오인증 비회원일 경우, 카카오인증 회원등록 절차를 거쳐 은행계좌 실명확인 절차를 밟은 다음 전자서명 가능
            isAllowSimpleRegistYN = False,

            # 수신자 실명확인 여부
            # true : 카카오페이가 본인인증을 통해 확보한 사용자 실명과 ReceiverName 값을 비교
            # false : 카카오페이가 본인인증을 통해 확보한 사용자 실명과 RecevierName 값을 비교하지 않음.
            isVerifyNameYN = True,

            # PayLoad, 이용기관이 생성한 payload(메모) 값
            PayLoad = 'Payload123'
        )

        response = kakaocertService.requestCMS(clientCode, requestObj, appUseYN)

        return render(request, 'responseCMS.html', {'receiptId': response.receiptId, 'tx_id': response.tx_id})
    except KakaocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})


def getCMSStatehandler(request):
    """
    자동이체 출금동의 요청시 반환된 접수아이디를 통해 서명 상태를 확인합니다.
    - https://www.kakaocert.com/docs/CMS/API/python#GetCMSState
    """
    try:
        # Kakaocert 이용기관코드, Kakaocert 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 자동이체 출금동의 요청시 반환받은 접수아이디
        receiptId = '022050912213500001'

        response = kakaocertService.getCMSState(clientCode, receiptId)

        return render(request, 'getCMSState.html', {'response': response})
    except KakaocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

def verifyCMShandler(request):
    """
    자동이체 출금동의 요청시 반환된 접수아이디를 통해 서명을 검증합니다.
    - 서명검증시 전자서명 데이터 전문(signedData)이 반환됩니다.
    - 카카오페이 서비스 운영정책에 따라 검증 API는 1회만 호출할 수 있습니다. 재시도시 오류처리됩니다.
    - https://www.kakaocert.com/docs/CMS/API/python#VerifyCMS
    """
    try:
        # Kakaocert 이용기관코드, Kakaocert 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 자동이체 출금동의 요청시 반환받은 접수아이디
        receiptId = '022050912213500001'

        # AppToApp 인증시, 앱스킴 성공처리시 반환되는 서명값(iOS-sig, Android-signature)
        # Talk Message 인증시 None 기재
        signature = None

        response = kakaocertService.verifyCMS(clientCode, receiptId, signature)

        return render(request, 'responseVerify.html', {'response': response})
    except KakaocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})
