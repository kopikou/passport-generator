<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import LayoutHCF from "components/LayoutHCF.vue";
import IndPlanUchNagrView from "pages/indPlan/components/IndPlanUchNagrView.vue";
import IndPlanPodgView from "pages/indPlan/components/IndPlanPodgView.vue";
import IndPlanUchMetWorkView from "pages/indPlan/components/IndPlanUchMetWorkView.vue";
import IndPLanOtherWorksView from "pages/indPlan/components/IndPLanOtherWorksView.vue";
import IndPlanWorkWithStudentsView from "pages/indPlan/components/IndPlanWorkWithStudentsView.vue";

const tab = ref('uchNagr');

const indPlan = ref([]);

async function getIndPlan(){
  let r = await api.get(`/api/indplan/self/`);
  indPlan.value = r.data;
}

onBeforeMount(async() => {
  await getIndPlan();
});
</script>

<template>
  <layout-h-c-f>
    <template #header>
      <q-tabs
        v-model="tab"
        class="text-teal"
      >
        <q-tab name="uchNagr" label="Учебная нагрузка" />
        <q-tab name="podg" label="Подготовка к учебным занятиям" />
        <q-tab name="uchMetWork" label="Учебно-методическая работа" />
        <q-tab name="otherWorks" label="Иные виды работ" />
        <q-tab name="workWithStudents" label="Работа с обучающимися и абитуриентами" />
      </q-tabs>
    </template>

    <template #content>
      <ind-plan-uch-nagr-view v-if="tab === 'uchNagr'" :rows="indPlan.uch_nagr"/>
      <ind-plan-podg-view v-if="tab === 'podg'" :rows="indPlan.podg"/>
      <ind-plan-uch-met-work-view v-if="tab === 'uchMetWork'"/>
      <ind-p-lan-other-works-view v-if="tab === 'otherWorks'"/>
      <ind-plan-work-with-students-view v-if ="tab === 'workWithStudents'"/>
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
