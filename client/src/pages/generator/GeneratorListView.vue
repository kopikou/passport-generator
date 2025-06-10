<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";

const generatorViewStore = useGeneratorViewStore();
const mainStore = useMainStore();

const {
  cafData,
  cafDataById,
} = storeToRefs(generatorViewStore)

const {
  mira_id,
} = storeToRefs(mainStore)

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

const $q = useQuasar()
const router = useRouter()
const listData = ref<GeneratorListData[]>([])
const uploadRpdFile = ref();

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

  return _(listData.value)
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
          items: items,
          types: _(items).map(x => x.type).flatten().uniq().value(),
          statuses: _(items).orderBy(x => STATUSES[x["status_verbose"]].index).groupBy('status_verbose').value(),
        }
      ]
    })
    .fromPairs()
    .value()
})

function clearFilter() {
  textFilter.value = ''
}

function toggleCanByCopiedByAnyone(id, item) {

}

async function getProgramData() {
  const loadingHelpers = $q.loading.show({
    group: 'first',
    message: 'Обновление списка дисциплин',
  })

  let r = await api.get("/api/generator/get-program-list/")
  listData.value = r.data

  loadingHelpers()
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

</script>

<template>
  <layout-h-c-f>
    <template #header>
      <div class="q-px-sm q-pb-sm">
        <div class="flex justify-between q-my-sm q-px-sm"
             style="display: grid; grid-template-columns: 1fr 220px auto; gap: 8px">
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
        </div>
      </div>
    </template>
    <template #content>
      <div style="height: 100%; overflow-y: auto">
        <div v-if="_.size(filteredListData) > 0" style="overflow: auto" class="full-height">
          <q-list bordered separator>
            <q-item
              class="q-pa-none"
              v-for="(item, index) in filteredListData"
              :key="index"
              dense
            >
              <q-item-section>
                <q-expansion-item
                  :label="item.abbr"
                  group="programs"
                >
                  <template #header>
                    <div class="q-item__section column q-item__section--main justify-center">
                      <div class="q-item__label">
                        <div style="display: flex; gap: 8px; justify-content: space-between">
                          <div style="display: flex; gap: 8px;">
                            <div style="width: 70px">{{ item.abbr }}</div>

                            <q-badge v-for="type in item.types">
                              {{ typeFilterLabel[type] }}
                            </q-badge>
                          </div>

                          <div style="display: flex; gap: 8px;">
                            <q-badge :text-color="STATUSES[status].textColor" :color="STATUSES[status].color"
                                     v-for="(status_items, status) in item.statuses">
                              {{ status }}: {{ status_items.length }}
                            </q-badge>
                          </div>
                        </div>
                      </div>
                    </div>
                  </template>
                  <q-card>
                    <q-card-section>
                      <div class="rpd-container">
                        <div class="rpd-row rpd-row__header text-weight-bold text-center">
                          <div>Код</div>
                          <div>Дисциплина</div>
                          <div>Составитель</div>
                          <div>Кафедра</div>
                          <div>Согласован</div>
                          <div>Утвержден</div>
                          <div>Статус</div>
                          <div>Управление</div>
                        </div>
                        <div v-for="i in item.items" :class="{[`status-${i.status}`]: true}" class="rpd-row rpd-row__body text-center">
                          <generator-list-view-item :item="i" @data-updated="getProgramData"/>
                        </div>
                      </div>
                    </q-card-section>
                  </q-card>
                </q-expansion-item>
              </q-item-section>
            </q-item>
          </q-list>
        </div>
        <div v-else class="text-h6 q-pa-md">
          <span v-if="_.size(listData) > 0">Не найдены дисциплины с текущими фильтрами</span>
          <span v-else>Дисциплины не назначены</span>
        </div>
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
  display: contents;

  &.status-0 > div { // "Назначен"
    background: white;
  }

  &.status-1 > div { // "Заполняется"
    background: $light-blue-1;
  }

  &.status-2 > div { // "Отправлен на проверку"
    background: $amber-1;
  }

  &.status-3 > div { // "Утвержден"
    background: $green-1;
  }

  &.status-4 > div { // "Требуются правки"
    background: $red-1;
  }


  $border: solid 1px silver;

  > div {
    padding: 0.5rem;
    border:  $border;
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
