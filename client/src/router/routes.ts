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
import RopListView from "pages/rop/RopListView.vue";
import RopView from "pages/rop/RopView.vue";
// import GeneratorMainView from "pages/generator/components/GeneratorMainView.vue";
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
import GeneratorGuidelinesView from "pages/generator/components/GeneratorGuidelinesView.vue";
import GeneratorFOSView from "pages/generator/components/GeneratorFOSView.vue";
import GeneratorTATView from "pages/generator/components/GeneratorTATView.vue";
import UploadView from "pages/upload/UploadView.vue";
import AspirantScientificPlansPage from "pages/scientificPlan/AspirantScientificPlansPage.vue";
// import AspirantScientificPlanView from "pages/scientificPlan/AspirantScientificPlanView.vue";
import PracticeGeneratorListView from "pages/generator/PracticeGeneratorListView.vue";
import GeneratorPracticeContent from "pages/generator/components/GeneratorPracticeContent.vue";
import GeneratorPracticeReportView from "pages/generator/components/GeneratorPracticeReportView.vue";
import GeneratorMainView from "pages/generator/components/GeneratorMainView.vue";
import ProfActivityView from "pages/activity/ProfActivityView.vue";
import ProfActivityItem from "pages/activity/components/ProfActivityItem.vue";
import RopMonitorView from "pages/rop/RopMonitorView.vue";
import IndPlanView from "pages/indPlan/IndPlanView.vue";
import IndPlanViewItem from "pages/indPlan/IndPlanViewItem.vue";

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: IndexPage,
  },
  {
    path: '/scientific-plan',
    meta: {
      permissions: [Permissions.can_use_generator],
    },
    children: [
      {
        path: '',
        name: 'ScientificPlans',
        component: AspirantScientificPlansPage,
      },
      {
        path: ':id',
        name: 'ScientificPlan',
        component: () => import("pages/scientificPlan/AspirantScientificPlanView.vue"),
        props: true,
      },
    ]
  },
  {
    path: '/practice_generator/',
    name: 'PracticeGeneratorListPage',
    meta: {
      permissions: [Permissions.can_use_generator],
    },
    children: [
      {
        path: '',
        name: "PracticeGeneratorListView",
        component: PracticeGeneratorListView,
      },
      {
        path: ':id',
        name: 'PracticeGeneratorView',
        component: GeneratorView,
        props: true,
        children: [
          {
            path: "main",
            name: "PracticeGeneratorMainView",
            component: GeneratorMainView,
          },
          {
            path: "competences",
            name: "PracticeGeneratorCompetencesView",
            component: GeneratorCompetenceView,
          },
          {
            path: "indicators",
            name: "PracticeGeneratorindicatorsView",
            component: GeneratorIndicatorsView,
          },
          {
            path: "structure",
            name: "PracticeGeneratorStructureView",
            component: GeneratorStructureView,
          },
          {
            path: "practice-content",
            name: "PracticeGeneratorContent",
            component: GeneratorPracticeContent,
          },
          {
            path: "practice-report",
            name: "PracticeGeneratorReport",
            component: GeneratorPracticeReportView,
          },
          {
            path: "library",
            name: "PracticeGeneratorLibraryView",
            component: GeneratorLibraryView,
          },
          {
            path: "soft",
            name: "PracticeGeneratorSoftwareView",
            component: GeneratorSoftwareView,
          },
          {
            path: "logistics",
            name: "PracticeGeneratorLogisticsView",
            component: GeneratorLogisticsView,
          },
          {
            path: "resources",
            name: "PracticeGeneratorResourcesView",
            component: GeneratorResourcesView,
          },
          {
            path: "guidelines",
            name: "PracticeGeneratorGuidelinesView",
            component: GeneratorGuidelinesView,
          },
          {
            path: "tat",
            name: "PracticeGeneratorTatView",
            component: GeneratorTATView,
          },
        ]
      },
    ]
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
            component: () => import("pages/generator/components/GeneratorMainView.vue"),
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
            path: "practice-content",
            name: "PracticeGeneratorContent",
            component: GeneratorPracticeContent,
          },
          {
            path: "practice-report",
            name: "PracticeGeneratorReport",
            component: GeneratorPracticeReportView,
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
          {
            path: "guidelines",
            name: "GeneratorGuidelinesView",
            component: GeneratorGuidelinesView,
          },
          {
            path: "fos",
            name: "GeneratorFOSView",
            component: GeneratorFOSView,
          },
          {
            path: "tat",
            name: "GeneratorTatView",
            component: GeneratorTATView,
          },
        ]
      },
    ]
  },
  {
    path: "/rop",
    name: "RopListView",
    // meta: {
    //   permissions: [rop],
    // },
    children: [
      {
        path: ':id',
        name: 'RopView',
        component: RopView
      }
    ]
  },
  {
    path: "/rop-monitor",
    name: "RopMonitorView",
    component: RopMonitorView,
    meta: {
      permissions: [Permissions.can_monitor_rops],
    }
  },
  {
    path: "/ind_plan",
    name: "IndPlanViewItem",
    component: IndPlanViewItem,
    // meta: {
    //   permissions: [rop],
    // },
    // children: [
    //
    // ]
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
  {
    path: "/upload",
    name: "UploadMainPage",
    children: [
      {
        path: '',
        name: 'UploadView',
        component: UploadView,
      },
    ]
  },
  {
    path: "/activity",
    name: "ProfActivityView",
    component: ProfActivityView,
    children: [{
      path: ':id',
      name: 'ProfActivityItem',
      component: ProfActivityItem,
      props: true,
    },
    ],
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
