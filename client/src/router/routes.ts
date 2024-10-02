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
import GeneratorCompetenceView from "pages/generator/components/GeneratorCompetenceView.vue";
import GeneratorIndicatorsView from "pages/generator/components/GeneratorIndicatorsView.vue";
import GeneratorDisciplinePlaceView from "pages/generator/components/GeneratorDisciplinePlaceView.vue";
import GeneratorStructureView from "pages/generator/components/GeneratorStructureView.vue";
import GeneratorDisciplineThemeView from "pages/generator/components/GeneratorDisciplineThemeView.vue";
import GeneratorDisciplineLabView from "pages/generator/components/GeneratorDisciplineLabView.vue";
import GeneratorDisciplinePracticeView from "pages/generator/components/GeneratorDisciplinePracticeView.vue";
import GeneratorDisciplineIndependentView from "pages/generator/components/GeneratorDisciplineIndependentView.vue";
import GeneratorLibraryView from "pages/generator/components/GeneratorLibraryView.vue";
import GeneratorSoftwareView from "pages/generator/components/GeneratorSoftwareView.vue";
import GeneratorLogisticsView from "pages/generator/components/GeneratorLogisticsView.vue";
import GeneratorDisciplineLecturesView from "pages/generator/components/GeneratorDisciplineLecturesView.vue";
import GeneratorResourcesView from "pages/generator/components/GeneratorResourcesView.vue";


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
          {
            path: "competences",
            name: "GeneratorCompetencesView",
            component: GeneratorCompetenceView,
          },
          {
            path: "indicators",
            name: "GeneratorindicatorsView",
            component: GeneratorIndicatorsView,
          },
          {
            path: "discipline-place",
            name: "GeneratorDisciplinePlaceView",
            component: GeneratorDisciplinePlaceView,
          },
          {
            path: "structure",
            name: "GeneratorStructureView",
            component: GeneratorStructureView,
          },
          {
            path: "discipline-theme",
            name: "GeneratorDisciplineThemeView",
            component: GeneratorDisciplineThemeView,
          },
          {
            path: "discipline-lectures",
            name: "GeneratorDisciplineLecturesView",
            component: GeneratorDisciplineLecturesView,
          },
          {
            path: "discipline-lab",
            name: "GeneratorDisciplineLabView",
            component: GeneratorDisciplineLabView,
          },
          {
            path: "discipline-practice",
            name: "GeneratorDisciplinePracticeView",
            component: GeneratorDisciplinePracticeView,
          },
          {
            path: "discipline-independent",
            name: "GeneratorDisciplineIndependentView",
            component: GeneratorDisciplineIndependentView,
          },
          {
            path: "library",
            name: "GeneratorLibraryView",
            component: GeneratorLibraryView,
          },
          {
            path: "soft",
            name: "GeneratorSoftwareView",
            component: GeneratorSoftwareView,
          },
          {
            path: "logistics",
            name: "GeneratorLogisticsView",
            component: GeneratorLogisticsView,
          },
          {
            path: "resources",
            name: "GeneratorResourcesView",
            component: GeneratorResourcesView,
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
