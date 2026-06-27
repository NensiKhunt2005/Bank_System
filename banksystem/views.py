from django.shortcuts import render,redirect
import random
from banksystem.models import sign_up,loan_type,loan_detail,loan_emi
from django.http import JsonResponse
import math
from django.urls import reverse


# loan_type.objects.create(loan_name="Gold",rate="9")
# loan_type.objects.create(loan_name="Home",rate="7.05")
# loan_type.objects.create(loan_name="Personal",rate="11")
# loan_type.objects.create(loan_name="Car",rate="7.30")
# loan_type.objects.create(loan_name="Educational",rate="8.55")

# Create your views here.

def dashboard(request):
    try:
        email=request.session['email1']
        t_bal=request.session['t_bal']
    except:
        return redirect('/')
    return render(request,'index.html',{'email':email,'bal':t_bal})
    


def signup(request):
    try:
        email=request.session['email1']
        return redirect('/dashboard/')
    except:
        msg=""
        if request.method=='POST':
            email=request.POST['email']
            password=request.POST['password']
            conf_password=request.POST['conf_password']
            contact=request.POST['contact']
            name=request.POST['name']
            deposit=request.POST['deposit']
            deposit=int(deposit)
            data1={'email':email,'password':password,'conf_password':conf_password,'contact':contact,'name':name,'deposit':deposit}

            if password==conf_password:
                acc_no=random.randrange(100000000000000,9999999999999999)
                data=sign_up(
                    email=email,
                    password=password,
                    conf_pass=conf_password,
                    contact=contact,
                    name=name,
                    deposit=deposit,
                    account_no=acc_no
                )
                request.session['email']=email
                request.session['password']=password
                request.session['acc_no']=acc_no
                if not sign_up.objects.filter(email=email) and not sign_up.objects.filter(contact=contact) and deposit>2000:
                    data.save()
                    return redirect('/')
                else:
                    if deposit<=2000:
                        msg="check your deposit amount.."
                        print("wrong")
                    else:
                        msg="check your email and contact.."
                    return render(request,'signup.html',{'data1':data1,'msg':msg})
                    
            else:
                msg="check your password.."
                return render(request,'signup.html',{'msg':msg,'data1':data1})
        return render(request,'signup.html')


def signin(request):
    try:
        email=request.session['email1']
        return redirect('/dashboard/')
    except:
        msg=""
        if request.method=='POST':
            email1=request.POST['email']
            password1=request.POST['Password']
            login_data=sign_up.objects.filter(email=email1,password=password1)
            if login_data.count()==1:
                request.session['email1']=email1
                bal=sign_up.objects.filter(email=email1).values()
                print(bal[0]['account_no'])
                request.session['acc_no']=bal[0]['account_no']
                t_bal={'deposit':bal[0]['deposit'],'name':bal[0]['name'],'acc':bal[0]['account_no']}
                request.session['t_bal']=t_bal
                request.session['dep_amt']=bal[0]['deposit']
                return redirect('/dashboard/')
            else:
                msg="check your email and password.."
                return render(request,'signin.html',{'msg':msg})
    return render(request,'signin.html')

def logout(request):
    del request.session['email1']
    return redirect('/')

def deposit(request):
    try:
        acc_no=request.session['acc_no']
        email=request.session['email1']
        data=sign_up.objects.filter(email=email).values()
        if request.method=='POST':
            s_acc_no=request.POST['acc_no']
            d_amt=request.POST['deposit']
            acc_no1=sign_up.objects.filter(account_no=s_acc_no).values()
            if acc_no1.count()==1:
                val=int(acc_no1[0]['deposit'])+int(d_amt)
                sign_up.objects.filter(account_no=s_acc_no).update(deposit=val)
                print(acc_no)
                print("s:",s_acc_no)
                if acc_no==int(s_acc_no):
                    request.session['dep_amt']=val
                return redirect('/dashboard/')
    except:
        return redirect('/')
    return render(request,'deposit.html')

def withdrawal(request):
    msg=''
    try:
        acc_no=request.session['acc_no']
        email=request.session['email1']
        data=sign_up.objects.filter(email=email).values()
        if request.method=='POST':
            s_acc_no=request.POST['acc_no']
            w_amt=request.POST['withdrawal']
            if acc_no==int(s_acc_no) :
                print("hello")
                acc_no1=sign_up.objects.filter(account_no=s_acc_no).values()
                if acc_no1.count()==1:
                    val=int(acc_no1[0]['deposit'])-int(w_amt)
                    print(val)
                    if val>=2000:
                        sign_up.objects.filter(account_no=s_acc_no).update(deposit=val)
                        request.session['dep_amt']=val
                        return redirect('/dashboard/')
                    else:
                        msg="you must have minimum 2000/- in your account and you have "+str(acc_no1[0]['deposit'])+"/-"
                        return render(request,'withdrawal.html',{'msg':msg})
            else:
                print("else")
                msg="you can not withdrawal from other account.."
                return render(request,'withdrawal.html',{'msg':msg})
    except :
        return redirect('/')
    return render(request,'withdrawal.html')

def term(request):
    return render(request,'terms_condition.html')

def loan(request):
    account_no=request.session['acc_no']
    data=loan_detail.objects.filter(account_no=account_no).values()
    print("data:",data.count())
    l_lenght=0
    if data:
        l_name=[]
        for i in range(len(data)):
            if len(data)<=3:
                l_name.append(data[i]['loan_name'])  
        print("l_name=",l_name) 
       
        if data.count()<=2: 
            l_lenght=len(l_name)
            print("l_lenght",l_lenght)
            return render(request,'loan.html',{'l_name':l_name,'l_lenght':l_lenght})

        return render(request,'loan.html',{'l_name':l_name})
    else:
        msg=''
        msg="No Previous Loan"
        return render(request,'loan.html',{'msg':msg,'l_lenght':l_lenght})
    
    return render(request,'loan.html')

def check_value(request,val):
    print("hello")
    return redirect('/dashboard/')

def loan_rate(request): 
    l_name = request.POST.get('key')
    data=loan_type.objects.filter(loan_name=l_name).values('rate')
    data1=data[0]
    request.session['l_name']=l_name 
    return JsonResponse(data1,safe=False)

def loan_rate1(request):
    account_no=request.session['acc_no']
    l_name=request.session['l_name']
    rate1=loan_type.objects.filter(loan_name=l_name).values('rate')
    rate1=rate1[0].values()
    yr=request.POST['yr']
    amt=int(request.POST['amt'])
    rate1=list(rate1)
    rate1=rate1[0]
    interest=(float(amt)*float(rate1)*float(yr))/100
    total=float(amt)+interest
    year=float(yr)*12
    amt=float(amt)
    f_rate=float(rate1)/(12*100)
    emi=(amt*f_rate*pow(1+f_rate,year))/(pow(1+f_rate,year)-1)
    final_emi=math.ceil(emi)
    print("emi:",final_emi)
    request.session['rate1']=rate1
    request.session['year']=year
    request.session['final_emi']=final_emi
    request.session['amt']=amt
    request.session['l_name']=l_name
    request.session['total_amt']=total
    data=loan_detail(
        loan_name=l_name,
        amount=amt,
        year=yr,
        rate=rate1,
        total_amt=total,
        emi=final_emi,
        account_no=account_no
    )
    return render( request,'loan_detail.html',{'data':data})

def final_emi(request):
    amt=request.session['amt']
    year=request.session['year']
    rate1=request.session['rate1']
    final_emi=request.session['final_emi']
    account_no=request.session['acc_no']
    l_name=request.session['l_name']
    total_amt=request.session['total_amt']
    bal=amt
    inter=[]
    p_amount=[]
    balance=[]
    emi_list=[]
    emi_id_list=[]
    year=int(year)
    existing=loan_detail.objects.filter(
        loan_name=l_name,
        amount=amt,
        year=year,
        rate=rate1,
        total_amt=total_amt,
        emi=final_emi,
        account_no=account_no
    )
    if existing.exists():
        msg1="You have already 3 loan..Please pay this loan then Bank will provide loan to you..\nThank you..!!"
        request.session['msg1']=msg1
        return redirect('/loan/')
    else: 
        emi_id=0 
        for i in range(year,0,-1):
            emi_id+=1
            s_i=(bal*rate1*year)/1200
            d=float(s_i)/year
            fractionnal_part=d-int(d)
            if fractionnal_part>=0.5:
                interest=math.ceil(float(s_i)/year)
            else:
                interest=math.floor(float(s_i)/year)

            p_amt=math.ceil(final_emi-interest)
            p_amount.append(p_amt)
            bal=math.ceil(bal-p_amt)
            if bal<0:
                bal=balance[-1]+bal
            inter.append(interest)
            balance.append(bal)
            emi_list.append(interest+p_amt)
            emi_id_list.append(emi_id)
            data1=loan_emi(
                EMI=final_emi,
                p_amt=p_amt,
                interest=interest,
                balance=bal,
                account_no=account_no,
                l_name=l_name,
                emi_id=emi_id
            )
            data1.save()  
            zipped_data=zip(emi_id_list,emi_list,p_amount,inter,balance)
        data=loan_detail(
            loan_name=l_name,
            amount=amt,
            year=year,
            rate=rate1,
            total_amt=total_amt,
            emi=final_emi,
            account_no=account_no
        )     
        data.save()
    return render( request,'all_emi.html',{'zip':zipped_data})    

def cut_emi(request):
    if request.method=="POST":
        emi_id=request.POST.get('pay')
        print(emi_id)
    return redirect('/final_emi/')
def display_emi(request):
    acc_no=request.session['acc_no']
    if request.method=="POST":
        l_name=request.POST.get('loan')
        emi=loan_emi.objects.filter(l_name=l_name,account_no=acc_no).values('EMI')
        emi=[item['EMI'] for item in emi]
        p_amt=loan_emi.objects.filter(l_name=l_name,account_no=acc_no).values('p_amt')
        p_amt=[item['p_amt'] for item in p_amt]
        interest=loan_emi.objects.filter(l_name=l_name,account_no=acc_no).values('interest')
        interest=[item['interest'] for item in interest]
        bal=loan_emi.objects.filter(l_name=l_name,account_no=acc_no).values('balance')
        bal=[item['balance'] for item in bal]
        emi_id=loan_emi.objects.filter(l_name=l_name,account_no=acc_no).values('emi_id')
        emi_id=[item['emi_id'] for item in emi_id]
        zipped_data=zip(emi_id,emi,p_amt,interest,bal)
    return render(request,'all_emi.html',{'zip':zipped_data})
