cell.set_facecolor('#F2F2F2') # Màu bạc nhạt cho Top 2
            elif key[0] == 3:
                cell.set_facecolor('#E6B8B8') # Màu đồng nhạt cho Top 3
            else:
                cell.set_facecolor('#FFFFFF') # Các hàng còn lại màu trắng

    # Thêm tiêu đề giải đấu nằm phía trên ảnh bảng điểm
    plt.title("🏆 BẢNG XẾP HẠNG GIẢI ĐẤU CUSTOM FREE FIRE 🏆", fontsize=14, weight='bold', pad=10, color='#D35400')

    # Lưu bảng điểm thành file ảnh tạm thời
    image_path = "bxh_output.png"
    plt.savefig(image_path, bbox_inches='tight', dpi=200)
    plt.close()
    return image_path

@bot.event
async def on_ready():
    print(f"🤖 Bot Vẽ Bảng Điểm Tự Động {bot.user} đã trực tuyến!")

@bot.command(name='done')
async def match_done(ctx, match_id: str):
    """Lệnh xong trận: !done [ID_Trận]"""
    await ctx.send(f"🔄 **[HỆ THỐNG]:** Đang nạp dữ liệu và tự động vẽ bảng xếp hạng cho trận `{match_id}`...")

    # 1. Tự động lấy kết quả từ server trận đấu về
    teams = get_garena_data(match_id)

    if not teams:
        return await ctx.send("❌ Lỗi dữ liệu trận đấu!")

    # 2. Tự động gom điểm, cộng dồn tích lũy
    for team in teams:
        name = team['name']
        rank = team['rank']
        kills = team['kills']

        t_points = FF_RANK_POINTS.get(rank, 0)
        k_points = kills * KILL_VALUE
        match_total = t_points + k_points

        if name not in tournament_bxh:
            tournament_bxh[name] = {'matches': 0, 'top_p': 0, 'kill_p': 0, 'total': 0}

        tournament_bxh[name]['matches'] += 1
        tournament_bxh[name]['top_p'] += t_points
        tournament_bxh[name]['kill_p'] += k_points
        tournament_bxh[name]['total'] += match_total

    # 3. Tự động gọi hàm vẽ ảnh bảng điểm
    img_file = draw_leaderboard_image()

    if img_file and os.path.exists(img_file):
        # 4. Gửi trực tiếp file ảnh bảng điểm cực đẹp lên phòng chat Discord
        await ctx.send(file=discord.File(img_file))
    else:
        await ctx.send("❌ Có lỗi xảy ra khi tự động xuất hình ảnh bảng điểm!")

@bot.command(name='bxh')
async def check_bxh_image(ctx):
    """Lệnh xem lại ảnh bảng xếp hạng hiện tại"""
    img_file = draw_leaderboard_image()
    if img_file:
        await ctx.send(file=discord.File(img_file))

@bot.command(name='clear')
async def clear_bxh(ctx):
    global tournament_bxh
    tournament_bxh = {}
    await ctx.send("🧹 Đã reset toàn bộ điểm số giải đấu!")

bot.run(os.getenv('DISCORD_TOKEN'))
