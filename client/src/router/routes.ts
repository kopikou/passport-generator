import {RouteRecordRaw} from 'vue-router';
import PlxListRpdView from "pages/plx/PlxListRpdView.vue";
import PlxFileView from 'pages/plx/PlxFileView.vue';
import GeneratorListView from "pages/generator/GeneratorListView.vue";
import IndexPage from "pages/IndexPage.vue";
import {Permissions} from "src/types";
import PlxDisciplineView from "pages/plx/components/PlxDisciplineView.vue";
import PlxDocumentsView from "pages/plx/components/PlxDocumentsView.vue";
import PlxIndicatorsView from "pages/plx/components/PlxIndicatorsView.vue";
import PlxSemesterView from "pages/plx/components/PlxSemesterView.vue";
import GeneratorView from "pages/generator/GeneratorView.vue";
import GeneratorMainView from "pages/generator/components/GeneratorMainView.vue";


const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: IndexPage,
  },
  {
    path: '/generator',
    name: 'GeneratorMainPage',
    meta: {
      permissions: [Permissions.can_use_generator],
    },
    children: [
      {
        path: '',
        name: 'GeneratorListView',
        component: GeneratorListView,
      },
      {
        path: ':id',
        name: 'GeneratorView',
        component: GeneratorView,
        props: true,
        children: [
          {
            path: "main",
            name: "GeneratorMainView",
            component: GeneratorMainView,
          },
        ]
      },
    ]
  },
  {
    path: "/plx",
    name: "PlxMainPage",
    meta: {
      permissions: [Permissions.can_upload_plx_files]
    },
    children: [
      {
        path: '',
        name: 'PlxListRpdView',
        component: PlxListRpdView,
      },
      {
        path: ':id',
        name: 'PlxViewFile',
        component: PlxFileView,
        props: true,
        children: [
          {
            path: "disciplines",
            name: "PlxDisciplineView",
            component: PlxDisciplineView
          },
          {
            path: "documents",
            name: "PlxDocumentsView",
            component: PlxDocumentsView
          },
          {
            path: "indicators",
            name: "PlxIndicatorsView",
            component: PlxIndicatorsView
          },
          {
            path: "semesters",
            name: "PlxSemesterView",
            component: PlxSemesterView
          }
        ]
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
