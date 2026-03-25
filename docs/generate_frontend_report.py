import os
import zipfile
from xml.sax.saxutils import escape


OUT_PATH = os.path.join("docs", "frontend_structure_report.docx")


PARAGRAPHS = [
    "AeroVision 前端代码结构说明",
    "一、文档目的",
    "本文档用于说明当前项目中前端相关代码的组织方式、各目录与代码文件的职责，以及前端需要对接的数据库接口与 YOLO 模型接口位置。项目整体采用 Django Templates 进行页面渲染，Bootstrap 统一视觉风格，少量 htmx 用于局部交互增强。",
    "二、项目总体前端构造",
    "1. 页面渲染方式：以后端 Django View + Template 为主，不采用前后端分离架构。",
    "2. UI 组织方式：公共布局放在 templates/base.html，导航与页脚拆分到 includes，模块页面按业务目录分别放置。",
    "3. 样式组织方式：全局样式集中在 static/css/app.css。",
    "4. 交互组织方式：基础交互和 htmx 事件处理集中在 static/js/app.js。",
    "5. 接口组织方式：页面访问走模板路由，前端联调接口主要由 uploads/api_views.py 提供 JSON API。",
    "三、根目录文件说明",
    "manage.py：Django 项目命令入口，用于 runserver、migrate、test 等操作。",
    "requirements.txt：项目 Python 依赖列表，包含 Django 和 modelscope 等依赖。",
    "README.md：项目说明文件。",
    "四、config 文件夹",
    "config/__init__.py：将 config 声明为 Python 包。",
    "config/settings.py：全局配置文件，定义 INSTALLED_APPS、模板目录、静态文件、媒体文件、登录跳转，以及 YOLO 默认模型配置 YOLO_DEFAULT_MODEL。",
    "config/urls.py：项目总路由入口，注册首页、账户、公告、反馈、文件管理以及 /api/ 接口路由。",
    "config/asgi.py：ASGI 启动入口。",
    "config/wsgi.py：WSGI 启动入口。",
    "五、core 文件夹",
    "core/__init__.py：将 core 声明为 Python 包。",
    "core/apps.py：core 应用配置。",
    "core/models.py：当前仅放置抽象时间戳基类 TimestampedModel，可供其它模型复用。",
    "core/views.py：负责首页、关于页、联系页的页面视图；首页还会读取公告摘要与上传统计数据。",
    "core/urls.py：core 模块路由，提供 /、/about/、/contact/。",
    "core/admin.py：后台管理注册预留文件，目前无具体管理项。",
    "core/tests.py：core 页面测试，验证首页、关于、联系页可访问。",
    "core/migrations/__init__.py：迁移包入口。",
    "六、accounts 文件夹",
    "accounts/__init__.py：将 accounts 声明为 Python 包。",
    "accounts/apps.py：accounts 应用配置。",
    "accounts/models.py：定义 UserProfile，用于补充 Django 默认用户之外的资料信息，如显示名称、职位、单位、简介、联系邮箱。",
    "accounts/forms.py：定义登录表单 LoginForm、注册表单 SignUpForm、资料编辑表单 UserProfileForm、安全设置表单 SecuritySettingsForm。",
    "accounts/views.py：实现注册、登录、退出、个人中心、资料编辑、安全设置（密码修改）等页面逻辑。",
    "accounts/urls.py：账户模块路由，包含 /login/、/signup/、/logout/、/profile/、/profile/edit/、/security/。",
    "accounts/admin.py：在 Django Admin 中注册 UserProfile，便于后台查看和维护用户资料。",
    "accounts/tests.py：账户页面测试，验证登录页和注册页可访问。",
    "accounts/migrations/0001_initial.py：UserProfile 的初始数据库迁移。",
    "accounts/migrations/__init__.py：迁移包入口。",
    "七、announcement 文件夹",
    "announcement/__init__.py：将 announcement 声明为 Python 包。",
    "announcement/apps.py：announcement 应用配置。",
    "announcement/models.py：当前直接复用 feedback.models.Announcement，目的是将公告展示模块独立出来而不重复定义数据表。",
    "announcement/views.py：实现公告列表页和公告详情页，专门承担对外展示公告的页面职责。",
    "announcement/urls.py：公告模块路由，提供 /announcements/ 与 /announcements/<id>/。",
    "announcement/admin.py：后台管理预留文件。",
    "announcement/tests.py：公告列表页测试。",
    "announcement/migrations/__init__.py：迁移包入口。",
    "八、feedback 文件夹",
    "feedback/__init__.py：将 feedback 声明为 Python 包。",
    "feedback/apps.py：feedback 应用配置。",
    "feedback/models.py：定义 Announcement 和 FeedbackEntry 两个模型。Announcement 用于公告数据存储；FeedbackEntry 用于反馈数据存储，包含姓名、邮箱、类型、内容、状态、提交用户、提交时间。",
    "feedback/forms.py：定义反馈提交表单 FeedbackForm 和反馈状态处理表单 FeedbackStatusForm。",
    "feedback/views.py：实现反馈提交、反馈列表、反馈详情、反馈状态更新逻辑。普通用户看到自己的反馈，管理员可以查看全部反馈并更新状态。",
    "feedback/urls.py：反馈模块路由，提供 /feedback/、/feedback/new/、/feedback/<id>/、/feedback/<id>/status/。",
    "feedback/admin.py：在 Django Admin 中注册 Announcement 与 FeedbackEntry，支持后台发布公告和处理反馈。",
    "feedback/tests.py：反馈页面测试。",
    "feedback/migrations/0001_initial.py：Announcement 与 FeedbackEntry 的初始数据库迁移。",
    "feedback/migrations/__init__.py：迁移包入口。",
    "九、dashboard 文件夹",
    "dashboard/__init__.py：将 dashboard 声明为 Python 包。",
    "dashboard/apps.py：dashboard 应用配置。",
    "dashboard/models.py：目前为空模型文件，作为后续工作台业务扩展预留。",
    "dashboard/views.py：工作台首页逻辑，汇总当前用户文件数量、反馈数量和公告数量，并展示近期数据。",
    "dashboard/urls.py：工作台路由，提供 /dashboard/。",
    "dashboard/admin.py：后台管理预留文件。",
    "dashboard/tests.py：工作台登录保护测试。",
    "dashboard/migrations/__init__.py：迁移包入口。",
    "十、uploads 文件夹",
    "uploads/__init__.py：将 uploads 声明为 Python 包。",
    "uploads/apps.py：uploads 应用配置。",
    "uploads/models.py：定义 UploadAsset，为文件管理和模型接口提供核心数据表。除了文件基础信息外，还包含 yolo_status、yolo_model_name、yolo_result、analyzed_at 等字段，用于保存 YOLO 推理状态和结果。",
    "uploads/forms.py：定义上传表单 UploadForm。",
    "uploads/views.py：实现文件列表、文件上传、文件详情等模板页面逻辑。详情页同时展示前端联调所需的 API 地址。",
    "uploads/urls.py：文件管理页面路由，提供 /uploads/、/uploads/new/、/uploads/<id>/。",
    "uploads/services.py：数据库序列化与 YOLO 服务抽象层。serialize_upload 用于把 UploadAsset 转成 JSON；BaseYoloGateway 定义推理网关接口；StubYoloGateway 是当前占位实现；run_yolo_prediction 负责执行推理并把结果写回数据库。",
    "uploads/api_views.py：最基本的前后端联调接口文件。这里提供上传列表接口、上传创建接口、上传详情接口、YOLO 分析触发接口、YOLO 配置信息接口。",
    "uploads/api_urls.py：JSON API 路由文件，统一挂载到 /api/ 前缀下。",
    "uploads/admin.py：在 Django Admin 中注册 UploadAsset。",
    "uploads/tests.py：上传模块测试，验证接口登录保护、文件上传和 YOLO 占位分析流程。",
    "uploads/migrations/0001_initial.py：UploadAsset 初始数据表迁移。",
    "uploads/migrations/0002_uploadasset_yolo_fields.py：为 UploadAsset 增加 YOLO 结果相关字段的迁移。",
    "uploads/migrations/__init__.py：迁移包入口。",
    "十一、common 文件夹",
    "common/__init__.py：将 common 声明为 Python 包。",
    "common/apps.py：common 应用配置。",
    "common/forms.py：定义 BootstrapFormMixin，用于给 Django 表单自动附加 Bootstrap 类名，减少模板中手动处理表单样式的工作。",
    "common/tests.py：公共模块测试占位文件。",
    "common/migrations/__init__.py：迁移包入口。",
    "十二、templates 文件夹",
    "templates/base.html：站点总布局模板，统一引入 Bootstrap、字体、全局 CSS、全局 JS、导航栏和页脚。",
    "templates/includes/navbar.html：公共导航栏模板。",
    "templates/includes/footer.html：公共页脚模板。",
    "templates/partials/status_panel.html：局部状态卡片模板，可用于 htmx 局部替换。",
    "templates/core/home.html：首页模板。",
    "templates/core/about.html：关于页模板。",
    "templates/core/contact.html：联系页模板。",
    "templates/accounts/login.html：登录页模板。",
    "templates/accounts/signup.html：注册页模板。",
    "templates/accounts/profile.html：个人中心模板。",
    "templates/accounts/profile_edit.html：个人资料编辑页模板。",
    "templates/accounts/security.html：安全设置模板，用于密码修改。",
    "templates/announcement/index.html：公告列表页模板。",
    "templates/announcement/detail.html：公告详情页模板。",
    "templates/feedback/index.html：反馈列表页模板。",
    "templates/feedback/form.html：反馈提交页模板。",
    "templates/feedback/detail.html：反馈详情页模板。",
    "templates/feedback/status_edit.html：反馈状态修改页模板。",
    "templates/dashboard/index.html：工作台首页模板。",
    "templates/uploads/index.html：文件管理列表模板。",
    "templates/uploads/form.html：文件上传模板。",
    "templates/uploads/detail.html：文件详情模板，同时向前端展示接口预留信息。",
    "十三、static 文件夹",
    "static/css/app.css：全局样式文件，负责整站配色、卡片样式、表单样式、动画和响应式表现。",
    "static/js/app.js：全局前端脚本，当前主要处理 htmx 请求前后的样式状态和局部替换后的动画效果。",
    "十四、数据库接口位置说明",
    "1. 账户相关数据库入口：accounts/models.py 中的 UserProfile。",
    "2. 公告与反馈数据库入口：feedback/models.py 中的 Announcement、FeedbackEntry。",
    "3. 文件管理与模型结果数据库入口：uploads/models.py 中的 UploadAsset。",
    "4. 前端联调时最常用的数据库数据出口：uploads/services.py 中的 serialize_upload，可将数据库对象转换成前端可直接消费的 JSON 结构。",
    "十五、YOLO 模型接口位置说明",
    "1. YOLO 接口抽象位置：uploads/services.py。",
    "2. 关键接口类：BaseYoloGateway。这个类定义了 predict(upload) 的调用约定，是未来接入真实 YOLO 模型的标准入口。",
    "3. 当前占位实现：StubYoloGateway。它不会调用真实模型，只返回一个结构稳定的假结果，便于前后端先对接。",
    "4. 写回数据库的执行函数：run_yolo_prediction(upload)。这个函数会更新 UploadAsset 的 yolo_status、yolo_model_name、yolo_result、analyzed_at。",
    "5. 对外 HTTP 接口入口：uploads/api_views.py。",
    "6. 前端可直接调用的 YOLO 相关接口：",
    "GET /api/yolo/：获取 YOLO 接口说明和路由信息。",
    "POST /api/uploads/<id>/analyze/：触发某个上传文件的 YOLO 推理占位流程。",
    "GET /api/uploads/<id>/：读取包含 YOLO 状态和 YOLO 结果的文件详情。",
    "十六、前端联调建议",
    "1. 页面渲染类前端工作优先使用模板文件和全局 CSS 完成。",
    "2. 如果后续要逐步增加异步能力，优先调用 /api/uploads/ 与 /api/uploads/<id>/analyze/。",
    "3. 等后端接入真实 YOLO 后，前端原则上不需要改接口地址，只需要根据返回的 yolo_status 和 yolo_result 渲染结果。",
    "十七、结论",
    "当前项目已经形成了完整的模板前端骨架，并且为数据库读写和 YOLO 模型对接预留了最基本的接口。前端开发可以在保持 Django 模板结构不变的前提下，继续完成页面细化、局部异步交互和结果展示。",
]


def make_paragraph(text: str) -> str:
    return (
        "<w:p><w:r><w:rPr><w:rFonts w:ascii=\"Calibri\" w:hAnsi=\"Calibri\" "
        "w:eastAsia=\"微软雅黑\"/><w:sz w:val=\"22\"/></w:rPr>"
        f"<w:t xml:space=\"preserve\">{escape(text)}</w:t></w:r></w:p>"
    )


def build_document_xml() -> str:
    body = "".join(make_paragraph(text) for text in PARAGRAPHS)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
 xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
 xmlns:v="urn:schemas-microsoft-com:vml"
 xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
 xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
 xmlns:w10="urn:schemas-microsoft-com:office:word"
 xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
 xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
 xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
 xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
 xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
 mc:Ignorable="w14 wp14">
 <w:body>
 {body}
 <w:sectPr>
   <w:pgSz w:w="11906" w:h="16838"/>
   <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>
 </w:sectPr>
 </w:body>
</w:document>"""


CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""


RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""


CORE_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>AeroVision Frontend Structure Report</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
</cp:coreProperties>"""


APP_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
</Properties>"""


def main() -> None:
    os.makedirs("docs", exist_ok=True)
    with zipfile.ZipFile(OUT_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", CONTENT_TYPES.encode("utf-8"))
        zf.writestr("_rels/.rels", RELS.encode("utf-8"))
        zf.writestr("word/document.xml", build_document_xml().encode("utf-8"))
        zf.writestr("docProps/core.xml", CORE_XML.encode("utf-8"))
        zf.writestr("docProps/app.xml", APP_XML.encode("utf-8"))
    print(os.path.abspath(OUT_PATH))


if __name__ == "__main__":
    main()
