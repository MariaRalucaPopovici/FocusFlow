models reflecting real objectives, admin-managed content (active flag = publish/unpublish), messages framework for validation feedback, input preservation UX, localStorage themes, login_required protection, and the admin↔database↔page round trip

Strategy.objects.filter(active=True) asks the ORM for only the strategies you've marked active — so you can "unpublish" a tip in admin without deleting it (that's a deliberate design choice worth mentioning in your report: admin controls what users see)
