from django.test import TestCase
import unittest
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from users.models import *
from users.views import *
from django.contrib.messages import get_messages

# ทดสอบกรณีของโมเดล Course
class CourseModelTest(TestCase):
    def setUp(self):
        # Create a course instance
        self.course = Course.objects.create(
            code="CN101",
            name="Intro to Computer Engineering",
            semester="2",
            academic_year=2024,
            seats=30
        )

    def test_course_str_method(self):
        # ทดสอบ the __str__ method output
        self.assertEqual(str(self.course), "CN101 - Intro to Computer Engineering")

    def test_course_default_is_quota_open(self):
        # ทดสอบ the default value of is_quota_open
        self.assertTrue(self.course.is_quota_open)

    def test_course_fields(self):
        #ตรวจสอบคุณสมบัติต่าง ๆ ของ Course ที่สร้างขึ้นใน setUp โดยเปรียบเทียบกับค่าที่คาดหวังไว้
        self.assertEqual(self.course.code, "CN101")
        self.assertEqual(self.course.name, "Intro to Computer Engineering")
        self.assertEqual(self.course.semester, "2")
        self.assertEqual(self.course.academic_year, 2024)
        self.assertEqual(self.course.seats, 30)


class QuotaRequestModelTest(TestCase):
    def setUp(self):
        # สร้าง user และ course เอาไว้ทดสอบ
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.course = Course.objects.create(
            code="CN101",
            name="Intro to Computer Engineering",
            semester="2",
            academic_year=2024,
            seats=30
        )
        # สร้าง quota_request เอาไว้ทดสอบ
        self.quota_request = QuotaRequest.objects.create(
            user=self.user,
            course=self.course
        )

    def test_quota_request_str_method(self):
        # ทดสอบ the __str__ method output
        self.assertEqual(str(self.quota_request), "testuser - Intro to Computer Engineering")

    def test_quota_request_default_is_approved(self):
        # ทดสอบ the default value of is_approved
        self.assertFalse(self.quota_request.is_approved)

    def test_quota_request_fields(self):
        #คำขอโควต้าถูกกำหนดให้เป็นของผู้ใช้ User ที่เราตั้งไว้จริง ๆ
        self.assertEqual(self.quota_request.user, self.user)
        #คำขอโควต้านี้เชื่อมโยงกับคอร์ส Course ที่เรากำหนดใน setUp 
        self.assertEqual(self.quota_request.course, self.course)

class RegisterViewTests(TestCase):
    def setUp(self):
        # สร้างผู้ใช้สำหรับการทดสอบ
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # สร้างคอร์สสำหรับการทดสอบ
        self.course = Course.objects.create(code='CN101', name='Intro to Computer Engineering',
                                            semester='1', academic_year=2023, seats=10)

#testing Signup_view(request) 
    def test_signup_view_get(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword'
        }) #ส่งคำขอ GET ไปยัง URL ของ view ที่ชื่อว่า 'logout' และเก็บผลลัพธ์ที่ได้จากการตอบกลับในตัวแปร response

        self.client.login(username='newuser', password='newpassword') #login 
        self.assertEqual(response.status_code, 200)  # redirect ไปยัง Signup ถูกต้อง

    def test_signup_view_uses_user_creation_form_get(self):
        response = self.client.get(reverse('signup'))                  # ตรวจสอบว่า GET request ส่ง UserCreationForm ไปยัง template
        self.assertEqual(response.status_code, 200)                    # ใช้ตรวจสอบว่า HTTP status code ที่ได้รับจาก response มีค่าเท่ากับ 200 ซึ่งเป็นค่า status code ที่บ่งบอกว่าคำขอสำเร็จ (HTTP 200 OK)
        self.assertIsInstance(response.context['form'], UserCreationForm)  # ตรวจสอบว่าใช้ UserCreationForm
        self.assertTemplateUsed(response, 'signup.html')                   #ใช้ template 'signup.html' ได้ถูกต้อง
    
    def test_signup_view_uses_user_creation_form_post(self):
        # ตรวจสอบว่า POST request ส่งข้อมูลผ่าน UserCreationForm 
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        })#สร้าง username, password
        self.assertEqual(response.status_code, 200)             # ใช้ตรวจสอบว่า HTTP status code ที่ได้รับจาก response มีค่าเท่ากับ 200 ซึ่งเป็นค่า status code ที่บ่งบอกว่าคำขอสำเร็จ (HTTP 200 OK)
        

    def test_signup_view_post_valid(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }) #ส่งคำขอ POST ไปยัง URL ของ view ที่ชื่อว่า 'login' โดยมีข้อมูลการล็อกอิน (username และ password) และเก็บผลลัพธ์ที่ได้จากการตอบกลับในตัวแปร response
        self.assertEqual(response.status_code, 302)                        # redirect ส่งผู้เข้าใช้ไปยัง URL ใหม่ 
        self.assertRedirects(response, reverse('course_list'))             # คาดหวังว่าจะเปลี่ยนเส้นทางไปยัง course_list
        self.assertTrue(User.objects.filter(username='newuser').exists())  # ตรวจสอบว่าผู้ใช้ถูกสร้างขึ้น


#testing login_view(request)
    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        }) #ส่งคำขอ POST ไปยัง URL ของ view ที่ชื่อว่า 'login' โดยมีข้อมูลการล็อกอิน (username และ password) และเก็บผลลัพธ์ที่ได้จากการตอบกลับในตัวแปร response
        self.assertEqual(response.status_code,302)             #redirect ส่งผู้เข้าใช้ไปยัง URL ใหม่   
        self.assertRedirects(response, reverse('course_list')) #redirect ไปยัง course_list
    
    def test_login_view_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)     # ใช้ตรวจสอบว่า HTTP status code ที่ได้รับจาก response มีค่าเท่ากับ 200 ซึ่งเป็นค่า status code ที่บ่งบอกว่าคำขอสำเร็จ (HTTP 200 OK)
        self.assertTemplateUsed(response, 'login.html') # ตรวจสอบว่าใช้ template ที่ถูกต้อง

    

#testing logout_view(request)
    def test_logout_view(self):
        response = self.client.get(reverse('logout'))     #คำสั่งนี้จะส่งคำขอ GET ไปยัง URL ของ view ที่ชื่อว่า 'logout' และเก็บผลลัพธ์ที่ได้จากการตอบกลับในตัวแปร response
        self.assertEqual(response.status_code, 302)       # redirect ส่งผู้เข้าใช้ไปยัง URL ใหม่   
        self.assertRedirects(response, reverse('login'))  # redirect ไปที่ login จริง

#testing course_list(request)
    def test_course_list_view(self):
        response = self.client.get(reverse('course_list'))    #ส่งคำขอ GET เพื่อออกจากระบบผู้ใช้ โดยเรียก URL ที่ถูกต้องตามชื่อที่ระบุใน urls.py
        self.assertEqual(response.status_code, 200)           # ใช้ตรวจสอบว่า HTTP status code ที่ได้รับจาก response มีค่าเท่ากับ 200 ซึ่งเป็นค่า status code ที่บ่งบอกว่าคำขอสำเร็จ (HTTP 200 OK)
        self.assertTemplateUsed(response, 'course_list.html') # ตรวจสอบว่าใช้ template ที่ถูกต้อง
        self.assertContains(response, self.course.name)       #ใช้เพื่อตรวจสอบว่าหน้าเว็บที่ถูกตอบกลับ response มีชื่อของคอร์สที่เราสร้างไว้ ("Intro to Computer Engineering")
    

#testing request_quota(request, course_id):
class RequestQuotaViewTest(TestCase):
    def setUp(self):
        # สร้าง user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # สร้าง course ที่เปิดรับโควต้าและมีที่นั่งว่าง
        self.available_course = Course.objects.create(
            code='CN101',
            name='Intro to Computer Engineering',
            semester='2',
            academic_year=2024,
            seats=10,  # มีที่นั่งว่าง
            is_quota_open=True
        )

        # สร้างคอร์สที่ไม่มีที่นั่งว่าง
        self.full_course = Course.objects.create(
            code='CN201',
            name='Java',
            semester='1',
            academic_year=2024,
            seats=0,  # ไม่มีที่นั่งว่าง
            is_quota_open=True
        )

    def test_request_quota_already_requested(self): #วิชาที่ขอโควต้าไปแล้ว
        QuotaRequest.objects.create(user=self.user, course=self.available_course, is_approved=True)  # สร้างคำขอโควต้าในฐานข้อมูล
        self.client.login(username='testuser', password='testpass') # ล็อกอินผู้ใช้
        response = self.client.post(reverse('request_quota', args=[self.available_course.id])) # ส่ง POST request ไปยัง request_quota
     
        self.assertEqual(response.status_code, 200) # ใช้ตรวจสอบว่า HTTP status code ที่ได้รับจาก response มีค่าเท่ากับ 200 ซึ่งเป็นค่า status code ที่บ่งบอกว่าคำขอสำเร็จ (HTTP 200 OK)
        self.assertTemplateUsed(response, 'error.html') #แสดงหน้าpage 'error.html'
        self.assertContains(response, 'You have already requested a quota for this course.') # เป็นข้อความที่จะส่งให้หน้าpage 'error.html'

    def test_request_quota_success(self): #ขอโควต้าสำเร็จ
        self.client.login(username='testuser', password='testpass') # ล็อกอินผู้ใช้
        response = self.client.post(reverse('request_quota', args=[self.available_course.id])) # ส่ง POST request ไปยัง request_quota

        # ตรวจสอบว่าได้รับ response ที่ถูกต้อง
        self.assertEqual(response.status_code, 302)  # redirect ส่งผู้เข้าใช้ไปยัง URL ใหม่ 
        self.assertRedirects(response, reverse('quota_success'))  # ตรวจสอบการเปลี่ยนเส้นทาง
        
        self.assertTrue(QuotaRequest.objects.filter(user=self.user, course=self.available_course).exists())# ตรวจสอบว่าคำขอโควต้าถูกสร้างขึ้นในฐานข้อมูล
        self.available_course.refresh_from_db()  # โหลดข้อมูลล่าสุดจากฐานข้อมูล
        self.assertEqual(self.available_course.seats, 9)  # ตรวจสอบว่าจำนวนที่นั่งลดลง

    def test_request_quota_full_seat(self): #กรณีที่โควต้าเต็ม
        # ล็อกอินผู้ใช้
        self.client.login(username='testuser', password='testpass')

        # ส่ง POST request ไปยัง request_quota สำหรับคอร์สที่เต็ม
        response = self.client.post(reverse('request_quota', args=[self.full_course.id]))

        # ตรวจสอบว่าได้รับ response ที่ถูกต้อง
        self.assertEqual(response.status_code, 200) # ใช้ตรวจสอบว่า HTTP status code ที่ได้รับจาก response มีค่าเท่ากับ 200 ซึ่งเป็นค่า status code ที่บ่งบอกว่าคำขอสำเร็จ (HTTP 200 OK)
        self.assertTemplateUsed(response, 'error.html') #แสดงหน้าpage 'error.html'
        self.assertContains(response, 'This subject has full seat. Please try again.') # เป็นข้อความที่จะส่งให้หน้าpage 'error.html'


#testing quota_success(request)
    def test_quota_success_view(self):
        response = self.client.get(reverse('quota_success'))
        self.assertEqual(response.status_code, 200) # ใช้ตรวจสอบว่า HTTP status code ที่ได้รับจาก response มีค่าเท่ากับ 200 ซึ่งเป็นค่า status code ที่บ่งบอกว่าคำขอสำเร็จ (HTTP 200 OK)
        self.assertTemplateUsed(response, 'quota_success.html') #แสดงหน้าpage 'quota_success.html'

#testing my_quota_requests(request)
class MyQuotaRequestsViewTest(TestCase): #ทดสอบโควต้าที่ขอ ผลลัพธ์เป็นได้หรือไม่ได้

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')  # สร้าง user    
        self.client.login(username='testuser', password='testpass') # ล็อกอิน user
        self.course = Course.objects.create(
            code='CN101',
            name='Intro to Computer Engineering',
            semester='2',
            academic_year=2024,
            seats=10,
            is_quota_open=True
        )# สร้าง Course เอาไว้ทดสอบ

    def test_my_quota_requests_with_approved_request(self):
        QuotaRequest.objects.create(user=self.user, course=self.course, is_approved=True) # สร้างคำขอโควต้าที่ได้รับการอนุมัติ
        response = self.client.get(reverse('my_quota_requests'))# ส่ง GET request ไปยัง my_quota_requests

        # ใช้ตรวจสอบว่า HTTP status code ที่ได้รับจาก response มีค่าเท่ากับ 200 ซึ่งเป็นค่า status code ที่บ่งบอกว่าคำขอสำเร็จ (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        #ใช้เพื่อตรวจสอบว่าเทมเพลต my_quota_requests.html ถูกใช้ในการสร้างหน้าเว็บที่ตอบกลับ (response) จากการเรียกใช้งาน view นั้น ๆ
        self.assertTemplateUsed(response, 'my_quota_requests.html')
        # ตรวจสอบว่าCourseแสดงในหน้าเว็บ
        self.assertContains(response, 'Intro to Computer Engineering')  
        
    def test_my_quota_requests_with_no_approved_requests(self):
        # กรณีที่ไม่มีคำขอโควต้าที่ได้รับการอนุมัติ
        response = self.client.get(reverse('my_quota_requests'))

        # ใช้ตรวจสอบว่า HTTP status code ที่ได้รับจาก response มีค่าเท่ากับ 200 ซึ่งเป็นค่า status code ที่บ่งบอกว่าคำขอสำเร็จ (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        #ใช้เพื่อตรวจสอบว่าเทมเพลต my_quota_requests.html ถูกใช้ในการสร้างหน้าเว็บที่ตอบกลับ (response) จากการเรียกใช้งาน view นั้น ๆ
        self.assertTemplateUsed(response, 'my_quota_requests.html')

#testing cancel_quota_request(request, request_id)
    def test_cancel_quota_request(self):
        #คำสั่งนี้จะสร้าง QuotaRequest ที่เชื่อมโยงผู้ใช้และคอร์สที่กำหนด พร้อมกับตั้งค่าสถานะ is_approved เป็น True และบันทึกข้อมูลนี้ลงในฐานข้อมูลทันที
        quota_request = QuotaRequest.objects.create(user=self.user, course=self.course, is_approved=True)

        #คำสั่งนี้จำลองการทำงานจริงของฟีเจอร์การยกเลิกคำขอโควต้า ซึ่งหลังจากคำสั่งนี้จะสามารถตรวจสอบการทำงานของระบบได้ 
        #เช่น ดูว่ามีการลบคำขอโควต้าออกจากฐานข้อมูลแล้วหรือไม่ และ URL มีการเปลี่ยนเส้นทางถูกต้อง
        response = self.client.post(reverse('cancel_quota_request', args=[quota_request.id]))

        # redirect หลังจากกด ยกเลิกขอโควต้า
        self.assertEqual(response.status_code, 302)  

        #คำสั่งนี้ทำให้มั่นใจได้ว่า เมื่อมีการยกเลิกคำขอโควต้า (QuotaRequest) เรียบร้อยแล้ว จะไม่มีข้อมูล QuotaRequest นี้หลงเหลืออยู่ในฐานข้อมูล
        self.assertFalse(QuotaRequest.objects.filter(id=quota_request.id).exists()) 

        # seats ควรจะกลับมา 10 ที่ เท่าเดิมเมื่อมีการยกเลิกการขอโควต้า
        self.assertEqual(self.course.seats, 10)  
      