from django.shortcuts import render
from django.http import HttpResponse
def home_page(request):
    print(request.POST, "WAZZAP")
    return render(request,
                  "home.html",{
                      "new_item_text": request.POST.get("item_text", ""),
                      # POST dictionary.get() return None if no match found by default, returns "" here
                  })