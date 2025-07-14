<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import {LocalStorage, SessionStorage, useQuasar} from "quasar";
import {GeneratorListData, GeneratorGroupsList} from "src/types";
import {storeToRefs} from "pinia";
import _ from "lodash";
import useMainStore from "stores/mainStore";
import LayoutHCF from "components/LayoutHCF.vue";
import GeneratorListViewItem from "pages/generator/components/GeneratorListViewItem.vue";

const mainStore = useMainStore();
const {
  rop
} = storeToRefs(mainStore)

const $q = useQuasar()
const listData = ref<GeneratorListData[]>([])

const groupsList = ref<GeneratorGroupsList[]>([]);

const currentData = ref(null);

const filesButtons = ref({
  rpd: {
    url: 'api/generator/get-rpd-done-info/',
    isLoading: false
  },
  oop: {
    url: 'api/generator/get-oop-done-info/',
    isLoading: false
  }
});

const typeFilterLabel = {
  rop:
    {
      title: 'Руководитель ОП',
      icon: 'mdi mdi-duck',
    },
  fac: {
    title: 'Директор',
    icon: 'mdi mdi-kangaroo',
  },
  zav: {
    title: 'Заведующий кафедры',
    icon: 'mdi mdi-bird',
  },
  person: {
    title: 'Разработчик РПД',
    icon: 'mdi mdi-koala',
  },
  view: {
    title: 'Просмотр РПД',
    icon: 'mdi mdi-linux',
  },
}

const STATUSES = {
  "Назначен": {
    color: "grey-2",
    textColor: "black",
    index: 1,
    title: "Назначен",
  },
  "Заполняется": {
    color: "cyan-5",
    textColor: "white",
    index: 2,
    title: "Заполняется",
  },
  "Требует моего согласования/утверждения": {
    color: "amber-6",
    textColor: "black",
    index: 3,
    title: "Требует моего согласования/утверждения",
  },
  "Отправлен на проверку": {
    color: "light-green-6",
    textColor: "white",
    index: 4,
    title: "Отправлен на проверку",
  },
  "Требуются правки": {
    color: "red-5",
    textColor: "white",
    index: 5,
    title: "Требуются правки",
  },
  "Утвержден": {
    color: "green-5",
    textColor: "white",
    index: 6,
    title: "Утвержден",
  },
}

const statusFilter = ref();
const groupFilter = ref($q.localStorage.getItem("surp_groupfilter") ? $q.localStorage.getItem("surp_groupfilter") : '')
const discplFilter = ref($q.localStorage.getItem("surp_discplfilter") ? $q.localStorage.getItem("surp_discplfilter") : '')
const myFilter = ref(LocalStorage.getItem('surp_myfilter') || 0)
const textFilter = ref<String>(LocalStorage.getItem('surp_rpdfilter') || '')

const filteredListData = computed(() => {

  let txtFilter = textFilter.value.trim().toLowerCase();
  let data = _(groupsList.value)
    .filter(x => {
      return (myFilter.value == 0 || x.type.includes('person'))
        && ((txtFilter == '' || (x.person || '').toLowerCase().includes(txtFilter))
          || (txtFilter == '' || x.abbr.toLowerCase().includes(txtFilter))
          || (txtFilter == '' || x.discode.toLowerCase().includes(txtFilter))
          || (txtFilter == '' || x.discpl.toLowerCase().includes(txtFilter)))
        && (!statusFilter.value || x.status_verbose == statusFilter.value)
    })
    .orderBy(x => [x.abbr, x.yr, x.discode], 'asc')
    .groupBy(x => `${x.abbr}-${x.yr.toString().slice(-2)}`)
    .toPairs()
    .map((item) => {
      let items = item[1];
      items.forEach(x => x.status = STATUSES[x["status_verbose"]].index);
      return [
        item[0],
        {
          abbr: item[0],
          plx_file: items[0].plx_file,
          // items: items,
          types: _(items).map(x => x.type).flatten().uniq().value(),
          statuses: _(items).orderBy(x => STATUSES[x["status_verbose"]].index).groupBy('status_verbose').value(),
        }
      ]
    })
    .fromPairs()
    .value()

  // if (txtFilter !== '' && currentData.value === null) {
  //   const firstKey = Object.keys(data)[0];
  //   currentData.value = data[firstKey];
  // } else if (currentData.value && data[currentData.value.abbr]) {
  //   currentData.value.items = data[currentData.value.abbr].items;
  // } else if (currentData.value && !data[currentData.value.abbr]) {
  //   currentData.value.items = [];
  // }

  return data
})

function clearFilter() {
  textFilter.value = ''
}


// async function getProgramData() {
//   const loadProgram = $q.loading.show({
//     group: 'programs',
//     message: 'Обновление списка дисциплин',
//   })

async function getGroupsList() {
  const loadProgram = $q.loading.show({
    group: 'programs',
    message: 'Обновление списка дисциплин',
  })

  let r = await api.get("/api/generator/get-group-list/")
  groupsList.value = r.data

  loadProgram()
}

watch([discplFilter, groupFilter, myFilter, textFilter], () => {
  $q.localStorage.setItem("surp_discplfilter", discplFilter.value)
  $q.localStorage.setItem("surp_groupfilter", groupFilter.value)
  $q.localStorage.setItem("surp_myfilter", myFilter.value)
  $q.localStorage.setItem("surp_rpdfilter", textFilter.value)
})

onBeforeMount(async () => {
  await getGroupsList()
  textFilter.value = ''
})

async function getDoneFile(key: string) {
  const fileUrl = filesButtons.value[key]['url'];

  filesButtons.value[key]['isLoading'] = true;

  const response = await api.get(fileUrl, {
     responseType: 'blob',
  });

  const fileName = getFileNameFromHeaders(response.headers) || 'document.xml';

  const url = window.URL.createObjectURL(
    new Blob([response.data], { type: 'application/xml' })
  );

  const link = document.createElement('a');
  link.href = url;
  link.download = fileName;
  link.style.display = 'none';

  document.body.appendChild(link);
  link.click();

  setTimeout(() => {
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    filesButtons.value[key]['isLoading'] = false;
  }, 100);
}

function getFileNameFromHeaders(headers) {
    const contentDisposition = headers['content-disposition'];
    if (!contentDisposition) return null;

    const fileNameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
    if (fileNameMatch && fileNameMatch[1]) {
      return fileNameMatch[1].replace(/['"]/g, '');
    }
    return null;
}

const columns = [
  { name: 'discode', align: 'center', label: 'Код', field: 'discode', sortable: true },
  { name: 'discpl', align: 'center', label: 'Дисциплина', field: 'discpl', sortable: true },
  { name: 'person', align: 'center', label: 'Составитель', field: 'razrab_name', sortable: true },
  { name: 'kaf', align: 'center', label: 'Кафедра', field: 'kafcode', sortable: true },
  { name: 'rukprog', align: 'center', label: 'Согласовал', field: 'rop_name', sortable: true },
  { name: 'zavkaf', align: 'center', label: 'Утвердил', field: 'zavkaf_name', sortable: true },
  { name: 'status_verbose', align: 'center', label: 'Статус', field: 'status_verbose', sortable: true },
  { name: 'control', align: 'center', label: 'Управление', field: 'type', sortable: false },
];

function rowClassFn (row) {
  return `rpd-row status-${row.status}`;
}

</script>

<template>
  <layout-h-c-f>
    <template #header>
      <div class="q-px-sm q-pb-sm">
        <div class="flex justify-between q-my-sm q-px-sm"
             style="display: grid; grid-template-columns: 1fr 220px auto auto auto; gap: 8px; align-items: center;">
          <q-input outlined label="Поиск по аббревиатуре, дисциплине, разработчику программы" v-model="textFilter"
                   clearable @clear="clearFilter"/>
          <!--        <q-input outlined label="Дисциплина" v-model="discplFilter"/>-->
          <q-select v-model="statusFilter"
                    label="Статус"
                    :options="_.map(STATUSES)"
                    option-label="title"
                    option-value="title"
                    emit-value
                    map-options
                    clearable
          />
          <q-toggle outlined label="Только мои" v-model="myFilter" :true-value="1" :false-value="0"/>

          <q-btn
            icon="mdi-file-excel"
            color="green-6"
            size="md"
            label="РПД"
            target="_blank"
            @click="getDoneFile('rpd')"
            :loading="filesButtons.rpd.isLoading"
            v-if="rop"
          />

          <q-btn
            icon="mdi-file-excel"
            color="green-6"
            size="md"
            label="ООП"
            target="_blank"
            @click="getDoneFile('oop')"
            :loading="filesButtons.oop.isLoading"
            v-if="rop"
          />
        </div>

        <div style="display: flex; flex-wrap: wrap; justify-content: start; gap: 8px;">
          <div v-for="status in STATUSES">
            <q-icon
              :color="status.color"
              name="square"
            />
            {{ status.title }}
          </div>
        </div>
      </div>
    </template>
    <template #content>
         <div v-if="_.size(filteredListData) > 0"
           style="display: grid; grid-template-columns: 300px 1fr; overflow: hidden;height: 100%"
      >
        <q-list
          style="overflow-y:auto; height: 100%; box-shadow: 0 0 8px silver; z-index: 100"
          separator
        >
          <q-item
            v-for="(value, key) in filteredListData"
            style="display: grid; gap: 8px;"
            clickable
            :active="currentData && currentData.abbr === key"
            @click="currentData = value"
            active-class="my-active-item"
          >
            <div style="display: grid; grid-template-columns: 1fr auto">
              <div style="display: flex; justify-content: left; font-size: 1.25rem;">
                {{ key }}
              </div>

              <div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: right; align-items: center">
                <q-badge v-for="type in value.types" class="animal-icon">
                  <i :class="typeFilterLabel[type].icon" ></i>

                  <q-tooltip style="font-size: 12px; background-color: white; color: black">
                    {{ typeFilterLabel[type].title}}
                  </q-tooltip>
                </q-badge>
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr auto">
              <div>
                <q-badge
                  :text-color="STATUSES[status].textColor"
                  :color="STATUSES[status].color"
                  v-for="(status_items, status) in value.statuses"
                  style="margin-right: 4px;"
                >
                  {{ status_items.length }}
                  <q-tooltip
                    style="font-size: 12px; background-color: white; color: black"
                  >
                    {{ status }}: {{ status_items.length }}
                  </q-tooltip>
                </q-badge>
              </div>

              <a :href="value.plx_file">*.plx</a>
            </div>

          </q-item>
        </q-list>

           <q-table
             v-if="currentData && currentData.items !== []"
            :rows="currentData.items"
            :columns="columns"
            virtual-scroll
            style="overflow-y: auto; height: 100%;"
            wrap-cells
            row-key="discode"
            flat
            bordered
            separator="cell"
            :rows-per-page-options="[0]"
            :table-row-class-fn="rowClassFn"
            table-header-class="table-header"
          >
            <template  v-slot:body="props">
              <q-tr :props="props">
                <generator-list-view-item @data-updated="getProgramData" :item="props.row"/>
              </q-tr>
            </template>
          </q-table>

        <span
          v-if="!currentData"
          style="align-content: center; text-align: center; font-size: 20px; font-weight: bold"
        >
          Выберите нужный раздел слева
        </span>
      </div>

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

.rpd-container {
  display: grid;
  grid-template-columns: auto repeat(5, 1fr) auto auto;
}

:deep(.rpd-row) {
  //display: contents;

  &.status-1 > td { // "Назначен"
    background: white;
  }

  &.status-2 > td { // "Заполняется"
    background: $light-blue-1;
  }

  &.status-3 > td { // "Требует моего согласования/утверждения"
    background: $amber-1;
  }

    &.status-4 > td { // "Отправлен на проверку"
    background: $green-1;
  }

  &.status-5 > td { // "Требуются правки"
    background: $red-1;
  }

  &.status-6 > td { // "Утвержден"
    background: $green-2;
  }




  $border: solid 1px silver;

  > div {
    padding: 0.5rem;
    border: $border;
    border-right: none;
    border-bottom: none;

    &:last-child {
      border-right: $border;
    }
  }

  &:last-child {
    > div {
      border-bottom: $border;
    }
  }

  &.rpd-row__body {
    //&:hover {
    //  > div {
    //    background: $info !important;
    //  }
    //}
  }

}

 :deep(.my-active-item) {
   background: $blue-grey-2;
 }

 :deep(.animal-icon){
   background: $grey-3;
   color: black;
   font-size: 18px;
   padding: 4px;
 }
</style>
