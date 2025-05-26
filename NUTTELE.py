from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import io
import asyncio
import nest_asyncio

BOT_TOKEN = '8086701406:AAGKpDDVNysglDTLCtrXSvdWw98DlsczVQs'

ADMIN_IDS = []

GMAIL_SENDER = "baoboi5328@gmail.com"
GMAIL_PASSWORD = "123789aA"
GMAIL_RECEIVER = "baoboi5328@gmail.com"

qr_image_data = None

def send_email_notification(subject, body):
    print(f"[Email notification disabled] Subject: {subject}, Body: {body}")

async def notify_admin(context: ContextTypes.DEFAULT_TYPE, text: str):
    print(f"[Notify admin disabled] {text}")

def format_user(user):
    username = f"@{user.username}" if user.username else "(chưa có username)"
    return f"{user.id} {username}"

async def load_qr_image():
    global qr_image_data
    if qr_image_data is None:
        with open(r'D:\BOT TELEGRAM\qr_vietcombank.jpg', 'rb') as f:
            qr_image_data = io.BytesIO(f.read())
    qr_image_data.seek(0)
    return qr_image_data

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await notify_admin(context, f"Người dùng {format_user(user)} đã bắt đầu bot bằng lệnh /start.")

    text = (
        "👋 *Shop Bảo Bối* xin chào..  ! \n"
        "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        "•\t*Ngoài bán mình cho tư bản ra thì nay em Bối còn bán thêm cả Bank Online & Tele Premium.*\n"
        "🔰\t*Bank Online*: Giao dịch nhanh chóng, an toàn, giá rẻ!\n"
        "🔰\t*Tele Premium*: Nick xịn, mõm hay, nâng tầm đẳng cấp!\n\n"
    )

    keyboard = [
        [InlineKeyboardButton("🚀  Telegram Premium", callback_data='premium')],
        [InlineKeyboardButton("🏦  Bank Online", callback_data='bank')],
        [
            InlineKeyboardButton("🎯 Báo Lỗi", url='https://t.me/lamgicoloi'),
            InlineKeyboardButton("☎️ ADMIN", url='https://t.me/boibank6789'),
            InlineKeyboardButton("💰 Nạp Tiền", callback_data='nap_tien'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        if update.callback_query.message and update.callback_query.message.text:
            await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup, parse_mode='Markdown')


async def handle_nap_tien(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await notify_admin(context, f"Người dùng {format_user(user)} đã xem thông tin Nạp Tiền.")

    photo = await load_qr_image()
    bank_info = (
        "Thông tin chuyển khoản:\n"
        "- Số tài khoản: 123456789\n"
        "- Chủ tài khoản: Nguyễn Văn A\n"
        "- Ngân hàng: Vietcombank\n\n"
        "⚠️ Vui lòng quét mã QR hoặc dùng thông tin trên để chuyển khoản  !!.\n "
    )

    keyboard = [
        [InlineKeyboardButton("✅   DONE   ✅", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=query.message.chat.id,
        photo=photo,
        caption=bank_info,
        reply_markup=reply_markup
    )

async def handle_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await notify_admin(context, f"Người dùng {format_user(user)} đã xem menu Premium.")

    text = (
        " 	            	  🛜 	*GÓI TELEGRAM PREMIUM* 	🛜\n"
        "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        "🔸 *1 tháng — 169.000đ* (Quá rẻ, trải nghiệm tuyệt vời ngay)\n"
        "🔸 *3 tháng — 369.000đ* (Tiết kiệm hơn, dùng thoải mái)\n"
        "🔸 *6 tháng — 569.000đ* (Trải nghiệm đỉnh cao, ko gián đoạn)\n"
        "🔸 *12 tháng — 869.000đ* (Siêu siêu hời, tiết kiệm cực lớn!)\n\n"
        "Chọn gói phù hợp để tiếp tục."    
    )

    keyboard = [
        [
            InlineKeyboardButton("1 Tháng", callback_data='order_premium_1'),
            InlineKeyboardButton("3 Tháng", callback_data='order_premium_3'),
            InlineKeyboardButton("6 Tháng", callback_data='order_premium_6'),
        ],
        [
            InlineKeyboardButton("12 Tháng", callback_data='order_premium_12'),
            InlineKeyboardButton("Kênh Sao", url='https://t.me/boibanvip'),
            InlineKeyboardButton("↩️ Quay lại", callback_data='main_menu')
        ],
    ]

    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')


async def handle_order_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    data = query.data
    period = data.split('_')[-1]

    prices = {
        '1': '169.000đ',
        '3': '369.000đ',
        '6': '569.000đ',
        '12': '869.000đ',
    }
    price = prices.get(period, 'Không xác định')

    descriptions = {
        '1': (
            "      💎 *Gói 1 tháng cao cấp* 💎\n"
            "• Tốc độ tải xuống nhanh hơn\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• Biểu tượng siêu ngầu, huy hiệu VIP\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• *Thanh Toán  :  169.000đ*\n"
        ),
        '3': (
            "      💎 *Gói 3 tháng cao cấp* 💎 \n"
            "• Tốc độ tải xuống nhanh hơn\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• Biểu tượng siêu ngầu, huy hiệu VIP\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• *Thanh Toán  :  369.000đ*\n"
        ),
        '6': (
            "      💎 *Gói 6 tháng cao cấp* 💎\n"
            "• Tốc độ tải xuống nhanh hơn\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• Biểu tượng siêu ngầu, huy hiệu VIP\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• *Thanh Toán  :  569.000đ*\n"
        ),
        '12': (
            "      💎 *Gói 12 tháng cao cấp* 💎\n"
            "• Tốc độ tải xuống nhanh hơn\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• Biểu tượng siêu ngầu, huy hiệu VIP\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• *Thanh Toán  :  869.000đ*\n"
        ),
    }

    description = descriptions.get(period, "Không có mô tả cho gói này.")

    text = f"*♦️Gói được chọn* *{period} tháng Premium  ♦️* \n\n{description}"

    keyboard = [
        [InlineKeyboardButton("🎁 Xác nhận mua gói này", callback_data='nap_tien')],
        [InlineKeyboardButton("↩️ Quay lại", callback_data='premium')]
    ]

    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')


async def handle_bank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await notify_admin(context, f"Người dùng {format_user(user)} đã xem menu Bank Online.")

    text = (
        "🏦 *Bank Online*\n"
        "Thông tin về dịch vụ Bank Online sẽ được cập nhật sớm.\n"
        "Vui lòng liên hệ ADMIN để biết thêm chi tiết."
    )
    keyboard = [
        [InlineKeyboardButton("↩️ Quay lại", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user = query.from_user

    if data not in ('premium', 'start_command', 'done_from_nap_tien'):
        context.user_data['previous_screen'] = data

    if data == 'nap_tien':
        await handle_nap_tien(update, context)
    elif data == 'done_from_nap_tien' or data == 'main_menu':
        previous = context.user_data.get('previous_screen')
        if not previous or data == 'main_menu':
            await start(update, context)
            return
        if previous == 'premium':
            await handle_premium(update, context)
        elif previous == 'bank':
            await handle_bank(update, context)  # <-- indent đã được sửa đúng
        elif previous and previous.startswith('order_premium_'):
            await handle_order_premium(update, context)
        else:
            await start(update, context)
    elif data == 'start_command':
        await notify_admin(context, f"Người dùng {format_user(user)} bấm nút DONE, trở về màn hình chính.")
        await start(update, context)
    elif data == 'back':
        await notify_admin(context, f"Người dùng {format_user(user)} bấm nút Back to Bot, quay lại màn hình trước đó.")
        previous = context.user_data.get('previous_screen', 'start_command')
        if previous == 'nap_tien':
            await handle_nap_tien(update, context)
        elif previous == 'premium':
            await handle_premium(update, context)
        elif previous and previous.startswith('order_premium_'):
            await handle_order_premium(update, context)
        else:
            await start(update, context)
    elif data == 'premium':
        await handle_premium(update, context)
    elif data and data.startswith('order_premium_'):
        await handle_order_premium(update, context)
    elif data == 'main_menu':
        await start(update, context)



async def main():
    nest_asyncio.apply()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot đã chạy...")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
