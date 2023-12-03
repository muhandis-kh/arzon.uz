
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
    1-muammo. Ma'lumotlarni scraping qilish uchun usul tanlash 
  </summary>
  <br>
  <ul>
      <li>
        Telegramdagi bir qancha kitob tarqatuvchi kanal va guruhlar bor va ulardagi kitob ma'lumotlarini yaratilgan model asosida ma'lumotlar omboriga qo'shish kerak. Albatta kitoblar fayllari 80 mingdan ko'p ekanligini hisobga olganda buni manual holatda bajarish imkonsiz
      </li>
      <li>
        Bu ma'lumotlarni python orqali yig'ib, uni kod orqali ma'lumotlar bazasiga qo'shmoqchi bo'ldim
      </li>
      <li>
        Buning uchun internetda mavjud bo'lgan resurslardan foydalanish uchun izlanish o'tkardim va bir nechta yechimlar ichidan https://github.com/estebanpdl/telegram-tracker bu repositoryda joylashgan koddan foydalanishga qaror qildim, sababi uchbu kod orqali bir nechta kanaldagi ma'lumotlarni bitta faylda to'plash mumkin edi. Bu esa kod orqali fayllarni boshqarishni osonlashtirdi
        Barcha ma'lumotlarni bitta faylda yig'ildani yaxshi lekin bu fayl hajmi githubning fayl limitidan oshib ketdi, men fayllarni ma'lumotlar bazasiga qo'shish uchun online serverdan foydalanmoqchiligim uchun u fayl github repo sida bo'lishi kerak edi. Men nega fayl hajmi bunchalik katta bo'lganligini sabablarini qidirdim. Fayl hajmi katta ekanligiga sabab yuqoridagi data scraper telegram kanaldagi barcha xabarlar ma'lumotlarini olib faylga joylagani edi ya'ni mening faylimda kanalga yuborilgan text, audio, reklama, sticker va shunga o'xshash xabarlarning barchasi mavjud edi. Men bu fayldagi ma'lumotlarni saralashim va fayl turiga qarab alohida faylga joylashim kerak edi. Buning uchun Pandas kutubxonasidan foydalandim, bunu ishlatishda internetdagi ma'lumotlar va ChatGPT katta yordam berdi.  
      </li>
      <li>
      Saralash yakunlangandan so'ng endi menda limitni oshmagan va faqatgina kerakli ma'lumotlardan tashkil topgan fayl bor edi. Buning natijasida online serverda ma'lumotlarni qo'shishim mumkin edi
      </li>
    </ul>
</details>

<details>  
  <summary>
    2-muammo. Fayllarni yagona telegram kanalda to'plash va ularning nomlarini lotin alifbosiga o'tkazish
  </summary>
    <br>
    <ul>
      <li>
        Loyihada kitob nomlari kirill va lotin alifbosida yozilgan edi va bu ma'lumotlar omboridan kitoblarni saralashda qiyinchilik tug'dirdi va kitob fayllari ko'plab kanallarda joylashganligi ularni yo'qolib qolish havfini oshirdi.
      </li>
      <li>
        Loyihadagi fayllarni saralash oson bo'lishi uchun fayllar ismini lotin alifbosiga o'tkazishim va fayllarni barchasini yagona telegram kanalda to'plashim kerak edi.
      </li>
      <li>
        Ma'lumotlar bazasiga model asosida kitob ma'lumotlarini kiritishdan oldin kitob nomlari kiril alifbosida ekanligi yoki emasligini tekshirishim kerak edi. Buning uchun internetdan yozuv alifbosini aniqlash uchun sodda funksiya topdim va uni ishlatib ko'rdim, hammasi joyida funksiya ishladi. Endi aniqlangan kirill alifbosidagi kitob nomlarini lotin alifbosiga o'tkazishim kerak edi. Buning uchun avvalroq eshitganim <a href="https://korrektor.uz/">korrektor.uz</a> loyihasidan foydalandim, to'g'risi loyiha asosida python kutubxonasi ishlab chiqilgani va korrektor.uz dan foydalanish Uzinfocom tufayli bepul bo'lgani menga juda qo'l keldi. Barcha fayl nomlari lotin alifbosida ma'lumotlar bazasiga joylanganidan so'ng bu ma'lumotlar asosida barcha fayllarni yagona telegram kanalda to'plash uchun telegram bot kodladim va uni ishga tushirdim.
      </li>
      <li>
        Bu ishlarning tufayli endi loyihadagi barcha fayl nomlari lotin alifbosida saqlangan va ularni saralash osonlashgan edi. Yana fayllar yo'qolib qolmasligi uchun barcha fayllar yagona telegram kanalda muvaffiqiyatli joylandi.
      </li>
    </ul>
</details>

Loyihani telegram orqali ham https://t.me/arzonro_bot ushbu bot orqali ishlatib ko'rishingiz mumkin. Xatoliklar haqida iltimos xabar bering.

Rahmat
