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
import {useQuasar} from "quasar";

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

const indPlan = ref();

const isAuthor = computed(() => {
  return indPlan.value.plan.user_created.user_id === userId.value;
});

const canAccepted = computed(() => {
  return indPlan.value.plan.zav === userId.value;
});

const canEdit = computed(() => {
  return isAuthor.value && indPlan.value.plan.status === 0;
})

const statuses = [
  {
    title: "Создан",
    color: "grey"
  },
  {
    title: "Ожидает рассмотрения",
    color: "orange-5"
  },
  {
    title: "Утвержден",
    color: "green"
  },
  {
    title: "Требуются правки",
    color: "red-5"
  },
];

const controlButtons = [
  {
    label: "Утвердить",
    permission: canAccepted,
    current_statuses: [1],
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
    current_statuses: [0, 3],
    next_status: 1,
    color: "orange-4",
    icon: "mdi-send-check-outline",
    text_color: "black",
  },
  {
    label: "Вернуть в редактирование",
    permission: isAuthor,
    current_statuses: [1],
    next_status: 0,
    color: "grey",
    icon: "mdi-pencil",
    text_color: "black",
  },
];

const $q = useQuasar();

async function getIndPlan(){
  const loadProgram = $q.loading.show({
    group: 'programs',
    message: 'Загрузка индивидуального плана',
  });

  const r = await api.get(`/api/indplan/${props.id}/`);
  indPlan.value = r.data;

  loadProgram();
}

onBeforeMount(async() => {
  await getIndPlan();
});

async function changeStatus(nextStatus: Number) {
  const formData = new FormData();
  formData.append('status', nextStatus.toString());

  const r  = await api.put(`/api/indplan/${props.id}/`, formData);

  indPlan.value.plan.status = r.data.status;
}

const sumOfHours = computed(() =>{
  let sum = 0;

  indPlan.value.uch_nagr.forEach(item => sum += item.items.reduce((acc, val) => acc + val.hours_count, 0));
  sum += indPlan.value.preparing.reduce((acc, val) => acc + parseFloat(val.hours_count), 0);
  sum += indPlan.value.educ_method.reduce((acc, val) => acc + val.hours_count, 0);
  sum += indPlan.value.other_works.reduce((acc, val) => acc + val.hours_count, 0);

  return sum;
});
</script>

<template>
  <layout-h-c-f v-if="indPlan !== undefined">
    <template #header>
      <div style="display: grid; grid-template-columns: auto auto auto; gap: 8px; margin: 8px; justify-content: space-between; align-items: center">
        <q-btn label="Назад" icon="mdi-arrow-left" to="/ind_plan/"/>

        <div style="display: grid; grid-template-columns: auto auto auto; gap: 8px; margin: 8px; justify-content: center; align-items: center">
          <span style="font-size: 15px">Автор: {{ indPlan.plan.user_created.last_name }} {{ indPlan.plan.user_created.first_name}} {{ indPlan.plan.user_created.middle_name }}</span>
          <q-badge :color="statuses[indPlan.plan.status].color" style="height: 20px; font-size: medium">{{ statuses[indPlan.plan.status].title }}</q-badge>

          <div style="display: flex; gap: 8px; align-items: center; margin: 8px;">
            <div v-for="button in controlButtons">
              <q-btn
                v-if="button.permission.value && button.current_statuses.includes(indPlan.plan.status)"
                :icon="button.icon"
                :color="button.color"
                :text-color="button.text_color"
                @click="changeStatus(button.next_status)"
              >
                <q-tooltip style="font-size: 12px; background-color: white; color: black">
                  {{ button.label }}
                </q-tooltip>
              </q-btn>
            </div>
          </div>
        </div>

        <div style=" margin: 8px; justify-content: center; align-items: center">
          <span style="font-size: 15px">Количество часов: {{ sumOfHours }}</span>
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
      <ind-plan-preparing-view v-if="tab === 'preparing'" :rows="indPlan.preparing" :canEdit="canEdit"/>
      <ind-plan-educ-method-work-view v-if="tab === 'educMethodWork'" :rows="indPlan.educ_method" :plan_id="props.id" :canEdit="canEdit"/>
      <ind-p-lan-other-works-view v-if="tab === 'otherWorks'" :rows="indPlan.other_works" :plan_id="props.id" :canEdit="canEdit"/>
      <ind-plan-work-with-students-view v-if ="tab === 'workWithStudents'" :rows="indPlan.work_with_students" :plan_id="props.id" :canEdit="canEdit"/>
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
