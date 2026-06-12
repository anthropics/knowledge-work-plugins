# Connectors

## วิธีที่ตัวแทนเครื่องมือทำงาน

Plugin นี้ใช้ `~~category` เป็น placeholder สำหรับเครื่องมือที่ผู้ใช้เชื่อมต่อในหมวดหมู่นั้นๆ เช่น `~~HRIS` อาจหมายถึง Workday, BambooHR หรือระบบ HRIS อื่นๆ ที่มี MCP server

Plugin นี้ **ไม่ผูกติดกับเครื่องมือใดโดยเฉพาะ** — อธิบาย workflow ในแง่ของหมวดหมู่ (HRIS, ATS, อีเมล ฯลฯ) แทนที่จะเป็นผลิตภัณฑ์เฉพาะ MCP server ใดๆ ในหมวดหมู่นั้นสามารถใช้งานได้

## Connectors สำหรับ Plugin นี้

| หมวดหมู่ | Placeholder | ตัวเลือก |
|---------|-------------|---------|
| ATS (ระบบสรรหา) | `~~ATS` | Greenhouse, Lever, Ashby, Workable |
| ปฏิทิน | `~~calendar` | Google Calendar, Microsoft 365 |
| แชท | `~~chat` | LINE Works, Slack, Microsoft Teams |
| อีเมล | `~~email` | Gmail, Microsoft 365 |
| HRIS (ระบบ HR) | `~~HRIS` | Workday, BambooHR, Rippling, Gusto |
| Knowledge Base | `~~knowledge base` | Notion, Confluence, Guru |
| ข้อมูลค่าตอบแทน | `~~compensation data` | Pave, Radford, Levels.fyi |

## ทักษะที่ได้ประโยชน์จากแต่ละ Connector

| Connector | ทักษะที่ได้รับประโยชน์ |
|-----------|---------------------|
| `~~HRIS` | ทุกทักษะ — ดึงข้อมูลพนักงาน, Grade Band, ประวัติ |
| `~~ATS` | recruiting-pipeline, draft-offer |
| `~~calendar` | onboarding — สร้างนัดหมายอัตโนมัติ |
| `~~chat` | people-report — แชร์สรุปรายงานในช่องทาง |
| `~~email` | draft-offer — ส่ง Offer Letter |
| `~~knowledge base` | policy-lookup — ค้นหา Handbook อัตโนมัติ |
| `~~compensation data` | comp-analysis — ดึงข้อมูลตลาดแบบ Real-time |
