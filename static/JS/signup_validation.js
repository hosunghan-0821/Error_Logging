   let id_check = false, nick_check = false;

    // 중복체크 버튼 클릭 시 실행 되는 함수
    $('#user_id_duplicate_check').click(function () {
        user_id_check()
    })

    // 비밀번호 다 입력하고 focus out 할 경우 실행 되는 함수
    $('#user_pw').focusout(function () {
        user_pw_check()
    })

    // 비밀번호 다 입력하고 focus out 할 경우 실행 되는 함수
    $('#user_pw_check').focusout(function () {
        user_pw_again_check()
    })

    $('#user_nickname_duplicate_check').click(function () {
        user_nickname_check()
    })

    //회원 아이디 유효성 검사 함수
    //TO-DO Ajax 이용해서, 아이디 중복 check 아직 미구현
    function user_id_check() {

        let user_id = $('#user_id').val()
        // 우선 중복 check ajax로 DB 연결해서 안겹치는거 확인한 후 , 그 뒤에 유효성 검사
        let formData = new FormData();
        // 우선 중복 check ajax로 DB 연결해서 닉네임 안겹치는거 확인한 후 , 그 뒤에 유효성 검사
        formData.append('check_item', "user_id")
        formData.append('check_value', user_id)
        $.ajax({
            type: "POST",
            url: "/check/duplicate",
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response['result'] == 'success') {
                    //정규식을 활용해서 특수문자 or 공백 거르는 IF문
                    if (user_id.search(/\W|\s/g) > -1) {
                        validation_false("user_id_message", "사용 불가능한 아이디 입니다.")
                        return false;
                    } else {
                        //사용자 특수문자 길이 확인하는 IF문
                        if (user_id.length >= 6 && user_id.length <= 12) {
                            validation_true("user_id_message", "사용 가능한 아이디 입니다.")
                            return true;
                        } else {
                            validation_false("user_id_message", "사용 불가능한 아이디 입니다.")
                            return false;
                        }
                    }
                } else {
                    validation_false("user_id_message", "중복된 아이디 입니다.")
                    return false;
                }
            }
        })


    }

    //회원 비밀번호 유효성 검사 함수
    function user_pw_check() {
        let user_pw = $('#user_pw').val()
        // 사용자 길이 6~20  , 특문 or 숫자1개 반드시 포함
        if (user_pw.search(/^(?=.*[a-zA-Z])((?=.*\d)|(?=.*\W)).{6,20}$/) > -1) {
            validation_true("user_pw_message", "사용 가능한 비밀번호입니다.")
            return true
        } else {
            validation_false("user_pw_message", "최소 1개의 숫자 혹은 특수 문자를 포함해야 함 길이 (6~20) ")
            return false
        }
    }

    //회원 비밀번호 일치하는지 검사 함수
    function user_pw_again_check() {
        let user_pw_again = $('#user_pw_check').val()
        let user_pw = $('#user_pw').val()
        if (user_pw === user_pw_again) {
            validation_true("user_pw_check_message", "비밀번호가 일치합니다.")
            return true
        } else {
            validation_false("user_pw_check_message", "비밀번호가 다릅니다.")
            return false
        }
    }

    //닉네임 중복 및 유효성 검사 함수
    //TO-DO Ajax 이용해서, 아이디 중복 check 아직 미구현
    function user_nickname_check() {

        const regex = /^[ㄱ-ㅎ|가-힣|a-z|A-Z|0-9|]+$/;

        let formData = new FormData();
        let user_nickname = $('#user_nickname').val()
        // 우선 중복 check ajax로 DB 연결해서 닉네임 안겹치는거 확인한 후 , 그 뒤에 유효성 검사
        formData.append('check_item', "user_nickname")
        formData.append('check_value', user_nickname)
        $.ajax({
            type: "POST",
            url: "/check/duplicate",
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {

                if (response['result'] == 'success') {
                    if (regex.test(user_nickname) === false) {
                        validation_false("user_nickname_message", "사용 불가능한 닉네임 입니다.")
                        return false;
                    } else {
                        if (user_nickname.length >= 2 && user_nickname.length <= 10) {
                            validation_true("user_nickname_message", "사용 가능한 닉네임 입니다.")
                            return true;
                        } else {
                            validation_false("user_nickname_message", "사용 불가능한 닉네임 입니다.")
                            return false;
                        }
                    }
                } else {
                    validation_false("user_nickname_message", "중복된 닉네임 입니다.")
                    return false;

                }

            }
        })


    }


    // 유효성 검사 후 각 div id에 작성될 message 작성
    function validation_true(id, message) {
        $('#' + id).removeClass('text-danger')
        $('#' + id).addClass('text-primary')
        $('#' + id).text(message)
        if (id === "user_id_message") {
            id_check = true
        } else if (id === "user_nickname_message") {
            nick_check = true
        }
    }

    function validation_false(id, message) {
        $('#' + id).removeClass('text-primary')
        $('#' + id).addClass('text-danger')
        $('#' + id).text(message)
        if (id === "user_id_message") {
            id_check = false
        } else if (id === "user_nickname_message") {
            nick_check = false
        }

    }


    function user_signup() {
        if (user_id_check() === false) {
            alert("id를 확인하세요")
            validation_false("user_id_message", "사용 불가능한 아이디 입니다.")
            return;
        } else if (user_pw_check() === false) {
            alert("pw를 확인하세요")
            validation_false("user_pw_message", "최소 1개의 숫자 혹은 특수 문자를 포함해야 함 길이 (6~20) ")
            return;

        } else if (user_pw_again_check() === false) {
            alert("pw를 확인하세요")
            validation_false("user_pw_check_message", "비밀번호가 다릅니다.")
            return;
        } else if (user_nickname_check() === false) {
            alert("닉네임을 확인하세요")
            validation_false("user_nickname_message", "사용 불가능한 닉네임 입니다.")
            return false;
        }
        // 다 통과했으면 서버로 전송
        else {
            setTimeout(() => {
                if (nick_check === true && id_check === true) {
                    let formData = new FormData();
                    let user_id = $('#user_id').val()
                    let user_pw = $('#user_pw').val()
                    let user_nickname = $('#user_nickname').val()
                    // 우선 중복 check ajax로 DB 연결해서 닉네임 안겹치는거 확인한 후 , 그 뒤에 유효성 검사
                    formData.append('user_pw', user_pw)
                    formData.append('user_id', user_id)
                    formData.append('user_nickname', user_nickname)
                    $.ajax({
                        type: "POST",
                        url: "/log/signup/verify",
                        data: formData,
                        contentType: false,
                        processData: false,
                        success: function (response) {
                            if (response['result'] == 'success') {
                                $.cookie('user_token',response['token'],{path:'/'})
                                window.location.replace('/')
                                alert("회원가입 성공")
                            }


                        }
                    })
                } else {
                    alert("회원정보를 다시 확인하세요")
                }

            }, 1000)


        }

    }