import { RouteRecordRaw } from 'vue-router';
import PlxUploadedView from "pages/PlxUploadedView.vue";
import listRpdView from "pages/listRpdView.vue";

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: listRpdView,
  },
  {
    path: '/upload',
    name: 'uploadFile',
    component: PlxUploadedView,
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
