from django.views.generic import ListView,DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article


class ArticleListView(LoginRequiredMixin,ListView):
	model=Article
	template_name='article_list.html'

class ArticleDetailView(LoginRequiredMixin,DetailView):
	model=Article
	template_name='article_detail.html'


class ArticleUpdateView(LoginRequiredMixin,UpdateView):
	model=Article
	fields=('title','body',)
	template_name='article_edit.html'

	def dispatch(self,request,*args,**kwargs):
		obj=self.get_object()
		if obj.author!=self.request.user:
			raise PermissionDenied
		return super().dispatch(request,*args,**kwargs)
	
	

class ArticleDeleteView(LoginRequiredMixin,DeleteView):
	model=Article
	template_name='article_delete.html'
	success_url=reverse_lazy('article_list')

	def dispatch(self,request,*args,**kwargs):
		obj=self.get_object()
		if obj.author!=self.request.user:
			raise PermissionDenied
		return super().dispatch(request,*args,**kwargs)

class ArticleCreateView(LoginRequiredMixin,CreateView):
	model=Article
	template_name='article_create.html'
	fields=('title','body',)

	def form_valid(self,form):
		form.instance.author=self.request.user
		return super().form_valid(form)
