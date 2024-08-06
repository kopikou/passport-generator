import {RouteRecordRaw} from 'vue-router';
import PlxUploadedView from "pages/plx/PlxUploadedView.vue";
import PlxListRpdView from "pages/plx/PlxListRpdView.vue";
import PlxFileView from 'pages/plx/PlxFileView.vue';
import GeneratorListView from "pages/generator/GeneratorListView.vue";
import IndexPage from "pages/IndexPage.vue";
import {Permissions} from "src/types";
import PlxIndexView from "pages/plx/PlxIndexView.vue";
import component from "*.vue";

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: IndexPage,
  },
  {
    path: '/generator',
    name: 'GeneratorListView',
    component: GeneratorListView,
    meta: {
      permissions: [],
    },
    children: []
  },
  {
    path: "/plx",
    name: "PlxMainPage",
    component: PlxIndexView,
    meta: {
      permissions: [Permissions.can_upload_plx_files]
    },
    children: [
      {
        path: 'list',
        name: 'PlxListRpdView',
        component: PlxListRpdView,
      },
      {
        path: 'upload',
        name: 'PlxUploadFiles',
        component: PlxUploadedView,
      },
      {
        path: ':id',
        name: 'PlxViewFile',
        component: PlxFileView,
        props: true,
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
