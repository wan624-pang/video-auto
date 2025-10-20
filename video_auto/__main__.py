from .sync import process_draft_automatically


def main() -> None:
    # 直接处理最新草稿，图片目录使用默认配置
    try:
        process_draft_automatically()
    except Exception as e:
        # 避免栈信息打爆日志，打印简洁错误
        print(f"处理草稿时出错: {e}")


if __name__ == "__main__":
    main()
