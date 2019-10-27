from django import template
register = template.Library()

@register.filter(name = "songtime")
def songtime(value):
	if value < 0:
		return "0:00"
	
	#return "{}{}:{}".format(("" if value / 60 > 10 else "0"), value / 60, value % 60)
	return "{}:{}{}".format(value / 60, ("" if value % 60 >= 10 else "0"), value % 60)
	