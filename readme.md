
# ARZON.uz (ishchi nomi)

> [!NOTE]
> Loyiha demo holatda

[![GitHub top language](https://img.shields.io/github/languages/top/muhandis-kh/arzon.uz?style=flat-square&logo=github)](https://github.com/muhandis-kh/arzon.uz)

## Loyiha haqida
Bu loyiha internet-do'konlaridan narxlarni solishtirish va ularni DRF orqali API holiga keltirish uchun yaratilgan.

Loyihani yaratishda bir nechta internet saytlaridan ma'lumotlarni olish uchun Selenium va BeatifulSoup ishlatildi, bazi saytlardan esa saytning foydalanuvchilar mahsulotni qidirishi uchun ishlatilgan API sidan foydalanildi. 

<details>
<summary>Foydalanilgan saytlar</summary>

<ol>
  
  <li>asaxiy.uz</li>
  <li>olcha.uz</li>
  <li>zoodmall.uz</li>
  <li>sello.uz</li>
  <li>texnomart.uz</li>
  
</ol>

</details>



Barcha taklif, savol va ogohlantirishlar uchun telegramdan <a href="https://t.me/khojimirzayev">menga</a> bog'lanishingiz mumkin.

Loyiha test rejimida ishlamoqda, iltimos xatoga duch kelganingizda menga xabar qiling.


> Bu loyiha hozir sinov bosqichidan o'tmoqda. Agarda biror xatolikka duchor
> bo'lsangiz, xatolik haqida [xabardor](https://github.com/muhandis-kh/arzon.uz/issues/new)
> qilishni unutmang.

Loyihani demo holatda https://arzon-uz.vercel.app/search-product/?query=query yoki https://arzon-uz.onrender.com/search-product/?query=query ushbu manzilga query o'rniga mahsulot nomini kiritish orqali ishlatib ko'rish mumkin. Loyiha bepul serverda joylashganligi va resurslar cheklanganligi uchun loyihadan foydalanish kunlik 10 ta so'rov bilan cheklangan.

## Loyihani ishlab chiqishda uchralgan qiyinchiliklar va yechimlari STAR metodi orqali
<details>
  <summary>
    1-muammo. Internet-do'konlaridan ma'lumotlarni yig'ish uchun mavjud uslublardan eng maqbuluni tanlash
  </summary>
  <br>
  <ul>
      <li>
        <i>Situation:</i> Internet-do'konlaridan ma'lumotlarni yig'ish uchun mavjud uslublardan eng maqbuluni tanlash
      </li>
      <li>
        <i>Task:</i> Ma'lumotlarni to'plash uchun bir necha usullar mavjud va ularning kamchilik va ustunliklarini taqqoslash kerak
      </li>
      <li>
       <i>Action:</i> Buning uchun mavjud usullarni o'rganishni boshladim. Internet saytini scraping qilish uchun ilk usullardan biri selenium, request va BeatifulSoup kutubxonalaridan foydalanish. Selenium afzalligi javascript kutubxonalari bilan hosil qilingan internet saytlaridan ham ma'lumotlarni olish mumkinligi edi lekin selenium loyihaning sekin ishlashiga sabab bo'lishi mumkin, shuni hisobga olgan holda avvalo ma'lumotlarni olmoqchi bo'lgan internet-do'konlaridan yuborilgan so'rovlar qaysi API ga yuborilganligini browserda developer tool orqali kuzatdim. Bu usul orqali asaxiy.uz dan tashqari qolgan internet-do'konlarda foydalanuvchi mahsulot qidirganda ishlatiladigan API manzilini topdim va API kutadigan headerslarni error messagelar orqali aniqlab, har bir sayt uchun sozladim. asaxiy.uz uchun avvaliga seleium bilan scraping qilish yo'llarini tanladim.   
      </li>
      <li>
     <i>Result:</i> Bu orqali loyihadagi asosiy muammo yechildi va keyingi qadamlar belgilandi
      </li>
    </ul>
</details>

<details>
  <summary>
    2-muammo. Asaxiy.uz uchun selenium bilan yozilgan funksiya loyiha tezligini sekinlashtirdi
  </summary>
  <br>
  <ul>
      <li>
        <i>Situation:</i> Asaxiy.uz uchun selenium orqali yozilgan funksiyalar bepul server internet-tezligi va saytlarning yuklanish uchun kutish vaqtlari uzun bo'lganligi uchun API ga yuborilgan so'rovdan javob kelishi 3-5 daqiqagacha cho'zildi
      </li>
      <li>
        <i>Task:</i> Muammoga sabab bo'lgan funksiyani request kutubxonasi bilan o'zgartirish
      </li>
      <li>
       <i>Action:</i> Ma'lumotlarni olish uchun selenium orqali qilingan funksiyani, request bilan o'zgartirdim, lekin sayt API siga ruhsat bo'lmaganligi uchun mahsulot qidirish linki orqali mahsulot ma'lumotlarini HTML ko'rinishida olib va ma'lumotlarni BeatifulSoup orqali ajratib oldim 
      </li>
      <li>
     <i>Result:</i> Funksiya o'zgartirilganidan so'ng serveridan javob kelishi 7-12 (25 barobar) soniyaga qadar tezlashdi, buning natijasida API tezligi sezilarli o'sdi 
      </li>
    </ul>
</details>

<details>
  <summary>
    3-muammo. Saytlarning ichki qidiruv tizimidagi muammolar
  </summary>
  <br>
  <ul>
      <li>
        <i>Situation:</i> Internet-do'konlarida qidiruv qilinganida eng arzon mahsulotlar eng boshida chiqadi va bu mening loyihamda kamchiliklarga sabab bo'ldi. Masalan Samsung A54 smartfoni qidirilganda Samsung A54 uchun himoya oynasi takliflari chiqdi
      </li>
      <li>
        <i>Task:</i> Muammoga sabab bo'lgan internet-do'kondagi mahsulotlarni API ga qo'shishdan oldin tekshiruv o'tkazish uchun funksiya yozish
      </li>
      <li>
       <i>Action:</i> Muammo kelib chiqgan internet-do'kondagi mahsulotlarni API ga qo'shishdan oldin, shu so'rov bo'yicha boshqa do'konlardagi mahsulotlar narxlari orasidan eng arzon mahsulot narxi belgilab olinib va muammoga sabab bo'lgan internet-do'kondagi mahsulot narxi bilan solishtirish va agar narxlar orasidagi farq katta bo'lsa API ma'lumotlariga qo'shmasligini ta'minlovchi tekshiruvchi funksiya yozildi
      </li>
      <li>
     <i>Result:</i> Buning natijasida foydalanuvchi mahsulot qidirganida so'rovga taaluqli bo'lgan mahsulotlar chiqishi ta'minlandi, API samaradorligi oshirildi
      </li>
    </ul>
</details>

Loyihani telegram orqali ham https://t.me/arzonro_bot ushbu bot orqali ishlatib ko'rishingiz mumkin. Xatoliklar haqida iltimos xabar bering.

<i><b>RAHMAT</b></i>
