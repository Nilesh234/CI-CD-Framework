#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { SampleStack } from './cdk-stack';

const app = new cdk.App();
new SampleStack(app, 'SampleStack', {});
