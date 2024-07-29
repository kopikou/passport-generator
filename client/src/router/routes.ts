import { RouteRecordRaw } from 'vue-router';
import PlxUploadedView from "pages/PlxUploadedView.vue";
import listRpdView from "pages/listRpdView.vue";
import PlxFileView from 'src/pages/PlxFileView.vue';
import GeneratorListView from "pages/GeneratorListView.vue";

const routes: RouteRecordRaw[] = [
  {
    path: '/upload/list',
    name: 'home',
    component: listRpdView,
  },
  {
    path: '/upload',
    name: 'uploadFile',
    component: PlxUploadedView,
  },
  {
    path: '/upload/view/:id',
    name: 'viewFile',
    component: PlxFileView,
    props: true,
  },
  {
    path: '/generator/list',
    name: 'generatorList',
    component: GeneratorListView,
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
