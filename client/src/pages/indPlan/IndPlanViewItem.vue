<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import LayoutHCF from "components/LayoutHCF.vue";
import IndPlanUchNagrView from "pages/indPlan/components/IndPlanUchNagrView.vue";

import IndPLanOtherWorksView from "pages/indPlan/components/IndPLanOtherWorksView.vue";
import IndPlanWorkWithStudentsView from "pages/indPlan/components/IndPlanWorkWithStudentsView.vue";
import IndPlanPreparingView from "pages/indPlan/components/IndPlanPreparingView.vue";
import IndPlanEducMethodWorkView from "pages/indPlan/components/IndPlanEducMethodWorkView.vue";
import useMainStore from "stores/mainStore";
import {storeToRefs} from "pinia";

const props = defineProps({
  id: {
    required: true,
  }
});

const mainStore = useMainStore();
const {
  userId,
} = storeToRefs(mainStore);

const tab = ref('uchNagr');

const indPlan = ref({});

const isAuthor = computed(() => {
  return indPlan.value.plan.user_created.user_id === userId.value
});

const statuses = [
  {
    title: "Создан",
    color: "grey"
  },
  {
    title: "Ожидает рассмотрения",
    color: "yellow"
  },
  {
    title: "Утвержден",
    color: "green"
  },
  {
    title: "Требуются правки",
    color: "red"
  },
];

const canAccepted = true;

const controlButtons = [
  {
    label: "Утвердить",
    permission: canAccepted,
    current_statuses: [1, 3],
    next_status: 2,
    color: "green",
    icon: "mdi-check",
    text_color: "black",
  },
  {
    label: "Отправить на доработку",
    permission: canAccepted,
    current_statuses: [1],
    next_status: 3,
    color: "red",
    icon: "mdi-repeat",
    text_color: "black",
  },
  {
    label: "Отправить на проверку",
    permission: isAuthor,
    current_statuses: [0],
    next_status: 1,
    color: "yellow",
    icon: "mdi-export-variant",
    text_color: "black",
  },
];

async function getIndPlan(){
  let r = await api.get(`/api/indplan/${props.id}/`);
  indPlan.value = r.data;
}

onBeforeMount(async() => {
  await getIndPlan();
});

async function changeStatus(nextStatus: Number) {
  const formData = new FormData();
  formData.append('status', nextStatus.toString());

  const r  = await api.put(`/api/indplan/${props.id}/`, formData);
}
</script>

<template>
  <layout-h-c-f>
    <template #header>
      <div style="display: grid; grid-template-columns: auto auto auto; gap: 20px; margin: 8px; justify-content: center; align-items: center">
        <span style="font-size: 20px">Автор: {{ indPlan.plan.user_created.last_name }} {{ indPlan.plan.user_created.first_name}} {{ indPlan.plan.user_created.middle_name }}</span>
        <q-badge :color="statuses[indPlan.plan.status].color" style="height: 40px; font-size: medium">{{ statuses[indPlan.plan.status].title }}</q-badge>

        <div>
          <div v-for="button in controlButtons">
            <q-btn v-if="button.permission && button.current_statuses.includes(indPlan.plan.status)" :icon="button.icon" :color="button.color" :text-color="button.text_color" @click="changeStatus(button.next_status)"/>
          </div>
        </div>
      </div>

      <q-tabs
        v-model="tab"
        class="text-teal"
      >
        <q-tab name="uchNagr" label="Учебная нагрузка" />
        <q-tab name="preparing" label="Подготовка к учебным занятиям" />
        <q-tab name="educMethodWork" label="Учебно-методическая работа" />
        <q-tab name="otherWorks" label="Иные виды работ" />
        <q-tab name="workWithStudents" label="Работа с обучающимися и абитуриентами" />
      </q-tabs>
    </template>

    <template #content>
      <ind-plan-uch-nagr-view v-if="tab === 'uchNagr'" :rows="indPlan.uch_nagr"/>
      <ind-plan-preparing-view v-if="tab === 'preparing'" :rows="indPlan.preparing"/>
      <ind-plan-educ-method-work-view v-if="tab === 'educMethodWork'" :rows="indPlan.educ_method" :plan_id="props.id"/>
      <ind-p-lan-other-works-view v-if="tab === 'otherWorks'" :rows="indPlan.other_works" :plan_id="props.id"/>
      <ind-plan-work-with-students-view v-if ="tab === 'workWithStudents'" :rows="indPlan.work_with_students" :plan_id="props.id"/>
    </template>
  </layout-h-c-f>
</template>

<style scoped lang="scss">
  :deep(.table-header) {
    position: sticky;
    z-index: 1;
    top: 0;
    background: $blue-grey-2;
  }
</style>
