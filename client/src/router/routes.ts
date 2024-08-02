import {RouteRecordRaw} from 'vue-router';
import PlxUploadedView from "pages/PlxUploadedView.vue";
import listRpdView from "pages/listRpdView.vue";
import PlxFileView from 'src/pages/PlxFileView.vue';
import GeneratorListView from "pages/GeneratorListView.vue";
import IndexPage from "pages/IndexPage.vue";
import {Permissions} from "src/types";

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: IndexPage,
  },
  {
    path: "/plx",
    name: "PlxMainPage",
    component: listRpdView,
    meta: {
      permissions: [Permissions.can_upload_plx_files]
    },
    children: [
      {
        path: '/upload',
        name: 'PlxUploadFiles',
        component: PlxUploadedView,
      },
      {
        path: '/upload/view/:id',
        name: 'PlxViewFile',
        component: PlxFileView,
        props: true,
      },
      {
        path: '/generator/list',
        name: 'PlxGeneratorList',
        component: GeneratorListView,
      },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
