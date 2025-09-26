<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import {LocalStorage, SessionStorage, useQuasar} from "quasar";
import {storeToRefs} from "pinia";
import _ from "lodash";
import useMainStore from "stores/mainStore";
import {useRouter} from "vue-router";

const router = useRouter();

// const $q = useQuasar();

const mainStore = useMainStore();
const {
  userId,
} = storeToRefs(mainStore);

const yearFilter = ref(null);

const textFilter = ref('');

const planType = ref('myPlans');
const typeOptions = [
  {
    label: 'Мои планы',
    value: 'myPlans',
  },
  {
    label: 'Все планы',
    value: 'allPlans',
  },
];

const planCategory = ref('currentPlans');
const categoryOptions = [
  {
    label: 'Текущие',
    value: 'currentPlans',
  },
  {
    label: 'Архив',
    value: 'oldPlans',
  },
];

const yearsList = computed(() => {
  let data = _(indPlanList.value)
      .map(item => {
        return item.year;
      })
      .value();

  data = [...new Set(data)]
  return data
});

const indPlanList = ref([]);

async function getIndPlans(){
  let r = await api.get(`/api/indplan/`);
  indPlanList.value = r.data;
}

onBeforeMount(async() => {
  await getIndPlans();
});

const columns = [
  { name: 'author', align: 'center', label: 'Автор', field: 'author', sortable: true },
  { name: 'year', align: 'center', label: 'Год', field: 'year', sortable: true },
  { name: 'status', align: 'center', label: 'Статус', field: 'status' },
];

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

const filteredIndPLanList = computed(() => {
  let txtFilter = textFilter.value.trim().toLowerCase();
  let data = _(indPlanList.value)
    .filter(x => {
      return ((planType.value === 'myPlans' && x.user_created.user_id === userId.value)
        || (planType.value === 'allPlans' && x.zav === userId.value))
          && (yearFilter.value === null || x.year === yearFilter.value)
          && (textFilter.value === ''
            || x.user_created.last_name.toLowerCase().includes(txtFilter)
            || x.user_created.first_name.toLowerCase().includes(txtFilter)
            || x.user_created.middle_name.toLowerCase().includes(txtFilter));
    })
    .value();

  return data;
})

// async function createIndPlan() {
//   const r = await api.post(`/api/indplan/`);
//
//   if (r.status === 400)
//       $q.notify({
//         message: r.data,
//         color: 'primary',
//         timeout: 10000
//       });
//   else
//     router.push(`/ind_plan/${r.data.id}/`);
// }

</script>

<template>
  <div style="display: grid; grid-template-columns: 5fr 2fr 2fr; gap: 8px; margin: 8px;">
    <q-input outlined label="Поиск по разработчику плана" v-model="textFilter"
                   clearable @clear="textFilter = ''"/>

    <q-select
      v-model="planType"
      :options="typeOptions"
      label="Тип планов"
      emit-value
      map-options
    />

    <q-select
      v-model="yearFilter"
      :options="yearsList"
      clearable
      label="Год"
      emit-value
      map-options
    />

<!--    <q-select-->
<!--      v-model="planCategory"-->
<!--      :options="categoryOptions"-->
<!--      label="Категория планов"-->
<!--      emit-value-->
<!--      map-options-->
<!--    />-->
  </div>

<!--  <q-btn-->
<!--    icon="mdi-plus-box"-->
<!--    color="green-6"-->
<!--    size="md"-->
<!--    style="margin: 8px"-->
<!--    @click="createIndPlan"-->
<!--    label="Создать план"-->
<!--  />-->

  <q-table
    :rows="filteredIndPLanList"
    :columns="columns"
    virtual-scroll
    style="overflow-y: auto; height: 100%;"
    wrap-cells
    flat
    bordered
    separator="cell"
    :rows-per-page-options="[0]"
    table-header-class="table-header"
  >
    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td key="author">
           <router-link :to="`/ind_plan/${props.row.id}/`">{{ props.row.user_created.last_name }} {{ props.row.user_created.first_name }} {{ props.row.user_created.middle_name }}</router-link>
        </q-td>

        <q-td key="year">
           {{ props.row.year }}
        </q-td>

        <q-td key="status" style="display: flex; justify-content: center; align-items: center">
          <q-badge :color="statuses[props.row.status].color" style="height: 20px; font-size: medium">{{ statuses[props.row.status].title }}</q-badge>
        </q-td>
      </q-tr>
    </template>
  </q-table>


</template>

<style scoped lang="scss">
  :deep(.table-header) {
    position: sticky;
    z-index: 1;
    top: 0;
    background: $blue-grey-2;
  }
</style>
