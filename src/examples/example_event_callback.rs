/*
    Copyright 2019 Supercomputing Systems AG
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/

///! Very simple example that shows how to subscribe to events.
use std::sync::mpsc::channel;

use clap::{load_yaml, App};
use codec::Decode;
use log::{debug, error};
use sp_core::sr25519;
use sp_core::H256 as Hash;

use std::fs::File;
use std::io::{Write, BufReader, BufRead, Error};
use std::io::BufWriter;

// This module depends on node_runtime.
// To avoid dependency collisions, node_runtime has been removed from the substrate-api-client library.
// Replace this crate by your own if you run a custom substrate node to get your custom events.
use node_template_runtime::Event;

use substrate_api_client::utils::FromHexString;
use substrate_api_client::Api;

fn write_hex<W: Write>(file: &mut BufWriter<W>, data: &[u8]) {
    for val in data {
        write!(file, "{:02X}", val);
    }
}


fn main() {
    let mut file = File::create("./events.txt").expect("create failed");
    //let mut file = BufWriter::new(file);
    env_logger::init();
    let url = get_node_url_from_cli();

    let api = Api::<sr25519::Pair>::new(url).unwrap();

    println!("Subscribe to events");
    let (events_in, events_out) = channel();
    api.subscribe_events(events_in).unwrap();

    loop {
        let event_str = events_out.recv().unwrap();

        let _unhex = Vec::from_hex(event_str).unwrap();
        let mut _er_enc = _unhex.as_slice();
        let _events = Vec::<system::EventRecord<Event, Hash>>::decode(&mut _er_enc);
        match _events {
            Ok(evts) => {
                for evr in &evts {
                    //println!("decoded: {:?} {:?}", evr.phase, evr.event);
                    match &evr.event {
                        Event::pallet_balances(be) => {
                            println!("\n>>>>>>>>>> balances event: {:?}", be);
                            write!(file, "{:?}\n", be);
                        }
                        Event::pallet_template(be) => {
                            println!("\n>>>>>>>>>> template event: {:?}", be);
                            write!(file, "{:?}\n", be);
                        }
                        _ => debug!("ignoring unsupported module event: {:?}", evr.event),
                    }
                }
            }
            Err(_) => error!("couldn't decode event record list"),
        }
    }
}

pub fn get_node_url_from_cli() -> String {
    let yml = load_yaml!("../../src/examples/cli.yml");
    let matches = App::from_yaml(yml).get_matches();

    let node_ip = matches.value_of("node-server").unwrap_or("ws://127.0.0.1");
    let node_port = matches.value_of("node-port").unwrap_or("9945");
    let url = format!("{}:{}", node_ip, node_port);
    println!("Interacting with node on {}", url);
    url
}
