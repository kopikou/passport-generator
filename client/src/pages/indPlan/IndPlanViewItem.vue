<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import LayoutHCF from "components/LayoutHCF.vue";
import IndPlanUchNagrView from "pages/indPlan/components/IndPlanUchNagrView.vue";

import IndPLanOtherWorksView from "pages/indPlan/components/IndPLanOtherWorksView.vue";
import IndPlanWorkWithStudentsView from "pages/indPlan/components/IndPlanWorkWithStudentsView.vue";
import IndPlanPreparingView from "pages/indPlan/components/IndPlanPreparingView.vue";
import IndPlanEducMethodWorkView from "pages/indPlan/components/IndPlanEducMethodWorkView.vue";

const props = defineProps({
  id: {
    required: true,
  }
})

const tab = ref('uchNagr');

const indPlan = ref([]);

async function getIndPlan(){
  let r = await api.get(`/api/indplan/${props.id}/`);
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
        <q-tab name="preparing" label="Подготовка к учебным занятиям" />
        <q-tab name="educMethodWork" label="Учебно-методическая работа" />
        <q-tab name="otherWorks" label="Иные виды работ" />
        <q-tab name="workWithStudents" label="Работа с обучающимися и абитуриентами" />
      </q-tabs>
    </template>

    <template #content>
      <ind-plan-uch-nagr-view v-if="tab === 'uchNagr'" :rows="indPlan.uch_nagr"/>
      <ind-plan-preparing-view v-if="tab === 'preparing'" :rows="indPlan.preparing"/>
      <ind-plan-educ-method-work-view v-if="tab === 'educMethodWork'" :rows="indPlan.preparing"/>
      <ind-p-lan-other-works-view v-if="tab === 'otherWorks'" :rows="indPlan.preparing"/>
      <ind-plan-work-with-students-view v-if ="tab === 'workWithStudents'" :rows="indPlan.work_with_students"/>
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
