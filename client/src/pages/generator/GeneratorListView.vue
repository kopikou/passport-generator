<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import {LocalStorage, SessionStorage, useQuasar} from "quasar";
import {GeneratorListData} from "src/types";
import {useRouter} from "vue-router";
import {storeToRefs} from "pinia";
import _ from "lodash";
import useMainStore from "stores/mainStore";
import GeneratorManageDialog from "pages/generator/components/dialogs/GeneratorManageDialog.vue";
import LayoutHCF from "components/LayoutHCF.vue";
import FileUploader from "pages/upload/components/FileUploader.vue";
import GeneratorListViewItem from "pages/generator/components/GeneratorListViewItem.vue";
 import { saveAs } from 'file-saver';

const generatorViewStore = useGeneratorViewStore();
const mainStore = useMainStore();

const {
  cafData,
} = storeToRefs(generatorViewStore)

const {
  mira_id,
} = storeToRefs(mainStore)

const $q = useQuasar()
const router = useRouter()
const listData = ref<GeneratorListData[]>([])

const currentData = ref(null);


const typeFilterLabel = {
  rop: 'Руководитель ОП',
  fac: 'Директор',
  zav: 'Заведующий кафедры',
  person: 'Разработчик РПД',
  view: 'Просмотр РПД',
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
    index: 3,
    title: "Отправлен на проверку",
  },
  "Требуются правки": {
    color: "red-5",
    textColor: "white",
    index: 4,
    title: "Требуются правки",
  },
  "Утвержден": {
    color: "green-5",
    textColor: "white",
    index: 5,
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
  let data = _(listData.value)
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
      return [
        item[0],
        {
          abbr: item[0],
          plx_file: items[0].plx_file,
          items: items,
          types: _(items).map(x => x.type).flatten().uniq().value(),
          statuses: _(items).orderBy(x => STATUSES[x["status_verbose"]].index).groupBy('status_verbose').value(),
        }
      ]
    })
    .fromPairs()
    .value()

  return data
})

function clearFilter() {
  textFilter.value = ''
}


async function getProgramData() {
  const loadProgram = $q.loading.show({
    group: 'programs',
    message: 'Обновление списка дисциплин',
  })

  let r = await api.get("/api/generator/get-program-list/")
  listData.value = r.data

  loadProgram()
}


function getRowColor(number) {
  return number % 2 == 0 ? 'bg-grey-3' : 'bg-white'
}


async function onFileDirectlyUploaded() {
  await getProgramData();
}

watch([discplFilter, groupFilter, myFilter, textFilter], () => {
  $q.localStorage.setItem("surp_discplfilter", discplFilter.value)
  $q.localStorage.setItem("surp_groupfilter", groupFilter.value)
  $q.localStorage.setItem("surp_myfilter", myFilter.value)
  $q.localStorage.setItem("surp_rpdfilter", textFilter.value)
})

onBeforeMount(async () => {
  await getProgramData()
})

async function getDoneFile(fileUrl: string) {
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
</script>

<template>
  <layout-h-c-f>
    <template #header>
      <div class="q-px-sm q-pb-sm">
        <div class="flex justify-between q-my-sm q-px-sm"
             style="display: grid; grid-template-columns: 1fr 220px auto auto auto; gap: 8px">
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
            color="green-6"
            size="md"
            label="Скачать РПД"
            target="_blank"
            @click="getDoneFile('api/generator/get-rpd-done-info/')"
          />

          <q-btn
            color="green-6"
            size="md"
            label="Скачать ООП"
            target="_blank"
            @click="getDoneFile('api/generator/get-oop-done-info/')"
          />
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
            clickable
            style="display: grid; grid-template-rows: auto auto; gap: 8px"
            :active="currentKey === key"
            @click="currentData = value"
          >
            <div style="display: grid; grid-template-columns: 100px 1fr">
              <div style="display: flex; justify-content: center; align-content: center; font-size: 1.25rem;">
                {{ key }}
              </div>

              <div style="display: flex; flex-wrap: wrap; gap: 8px">
                <q-badge v-for="type in value.types">
                  {{ typeFilterLabel[type] }}
                </q-badge>
              </div>
            </div>

            <div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: start">
              <q-badge
                :text-color="STATUSES[status].textColor"
                :color="STATUSES[status].color"
                v-for="(status_items, status) in value.statuses"
              >
                {{ status_items.length }}
                <q-tooltip
                  style="font-size: 12px; background-color: white; color: black"
                >
                  {{ status }}: {{ status_items.length }}
                </q-tooltip>
              </q-badge>
            </div>
          </q-item>
        </q-list>

        <generator-list-view-item v-if="currentData !== null" :items="currentData.items"/>

        <span
          v-if="currentData === null"
          style="align-content: center; text-align: center; font-size: 20px; font-weight: bold"
        >
          Выберите нужный раздел слева
        </span>
      </div>

    </template>
  </layout-h-c-f>

</template>

<style scoped lang="scss">
.rpd-container {
  display: grid;
  grid-template-columns: auto repeat(5, 1fr) auto auto;
}

:deep(.rpd-row) {
  //display: contents;

  &.status-0 > td { // "Назначен"
    background: white;
  }

  &.status-1 > td { // "Заполняется"
    background: $light-blue-1;
  }

  &.status-2 > td { // "Отправлен на проверку"
    background: $amber-1;
  }

  &.status-3 > td { // "Утвержден"
    background: $green-1;
  }

  &.status-4 > td { // "Требуются правки"
    background: $red-1;
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

</style>
